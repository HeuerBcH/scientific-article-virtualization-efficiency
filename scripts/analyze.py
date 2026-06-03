#!/usr/bin/env python3
"""
analyze.py — Statistical analysis of memory access pattern benchmarks.

Reads:  data/raw/results.csv
Writes: data/processed/summary.csv
        data/processed/hypothesis_tests.csv
        data/processed/pairwise_tests.csv

Statistical procedure:
  1. Per-group descriptive statistics (mean, median, std, CV, 95% CI).
  2. Shapiro-Wilk normality test (n=30 per group, alpha=0.05).
  3. If all groups normal → one-way ANOVA; else → Kruskal-Wallis.
  4. Post-hoc pairwise comparisons via Dunn's test (non-parametric,
     Bonferroni correction) or Tukey HSD (parametric).

Run from project root:
    python3 scripts/analyze.py
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import shapiro, kruskal, f_oneway
from itertools import combinations

# ---------------------------------------------------------------------------
ALPHA     = 0.05
RAW_CSV   = os.path.join('data', 'raw', 'results.csv')
OUT_DIR   = os.path.join('data', 'processed')
METRIC    = 'bandwidth_gbs'   # primary metric for hypothesis testing
METRIC2   = 'ns_per_element'  # secondary metric (latency)
# ---------------------------------------------------------------------------


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Synthesize a human-readable group label
    def make_group(row):
        if row['pattern'] == 'stride':
            return f"stride_{int(row['stride'])}"
        elif row['pattern'] == 'block':
            kb = int(row['block_bytes'] // 1024)
            return f"block_{kb}KB"
        else:
            return row['pattern']
    df['group'] = df.apply(make_group, axis=1)
    return df


def describe_group(series: pd.Series) -> dict:
    n   = len(series)
    m   = series.mean()
    med = series.median()
    s   = series.std(ddof=1)
    sem = stats.sem(series)
    t_crit = stats.t.ppf(1 - ALPHA / 2, df=n - 1)
    return {
        'n':         n,
        'mean':      m,
        'median':    med,
        'std':       s,
        'cv_pct':    (s / m * 100) if m != 0 else np.nan,
        'ci95_low':  m - t_crit * sem,
        'ci95_high': m + t_crit * sem,
        'min':       series.min(),
        'max':       series.max(),
    }


def compute_summary(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    records = []
    for (group, size_label), sub in df.groupby(['group', 'size_label']):
        rec = {'group': group, 'size_label': size_label}
        rec.update(describe_group(sub[metric]))
        rec['metric'] = metric
        records.append(rec)
    return pd.DataFrame(records)


def normality_report(df: pd.DataFrame, metric: str) -> pd.DataFrame:
    records = []
    for (group, size_label), sub in df.groupby(['group', 'size_label']):
        vals = sub[metric].values
        if len(vals) < 3:
            continue
        stat, p = shapiro(vals)
        records.append({
            'group':       group,
            'size_label':  size_label,
            'n':           len(vals),
            'shapiro_W':   stat,
            'shapiro_p':   p,
            'normal':      p > ALPHA,
        })
    return pd.DataFrame(records)


def run_omnibus(groups_data: list, all_normal: bool) -> dict:
    """One-way ANOVA or Kruskal-Wallis depending on normality."""
    if all_normal and len(groups_data) >= 2:
        stat, p = f_oneway(*groups_data)
        return {'test': 'one_way_ANOVA', 'statistic': stat, 'p_value': p}
    elif len(groups_data) >= 2:
        stat, p = kruskal(*groups_data)
        return {'test': 'Kruskal-Wallis', 'statistic': stat, 'p_value': p}
    return {'test': 'insufficient_groups', 'statistic': np.nan, 'p_value': np.nan}


def dunn_pairwise(df: pd.DataFrame, group_col: str, metric: str) -> pd.DataFrame:
    """
    Dunn's post-hoc test with Bonferroni correction.
    Non-parametric pairwise comparison after a significant Kruskal-Wallis.
    """
    groups = df[group_col].unique()
    n_comparisons = len(groups) * (len(groups) - 1) // 2
    records = []

    all_vals = df[metric].values
    all_ranks = stats.rankdata(all_vals)
    df = df.copy()
    df['_rank'] = all_ranks
    N = len(all_vals)

    for g1, g2 in combinations(groups, 2):
        r1 = df[df[group_col] == g1]['_rank'].values
        r2 = df[df[group_col] == g2]['_rank'].values
        n1, n2 = len(r1), len(r2)
        if n1 == 0 or n2 == 0:
            continue
        mean_r1 = r1.mean()
        mean_r2 = r2.mean()
        # Standard error for Dunn statistic
        se = np.sqrt((N * (N + 1) / 12.0) * (1.0 / n1 + 1.0 / n2))
        z  = (mean_r1 - mean_r2) / se
        p_raw  = 2 * (1 - stats.norm.cdf(abs(z)))
        p_bonf = min(p_raw * n_comparisons, 1.0)
        records.append({
            'group_a':   g1,
            'group_b':   g2,
            'z_stat':    z,
            'p_raw':     p_raw,
            'p_bonferroni': p_bonf,
            'significant': p_bonf < ALPHA,
        })
    return pd.DataFrame(records)


def analyse_size(df_size: pd.DataFrame, size_label: str, metric: str) -> tuple:
    """Run full statistical pipeline for one size level. Returns (omnibus_row, pairwise_df)."""
    norm_df    = normality_report(df_size, metric)
    all_normal = norm_df['normal'].all() if len(norm_df) > 0 else False

    groups      = df_size['group'].unique()
    groups_data = [df_size[df_size['group'] == g][metric].values for g in groups]

    omnibus = run_omnibus(groups_data, all_normal)
    omnibus.update({
        'size_label':       size_label,
        'metric':           metric,
        'n_groups':         len(groups),
        'all_normal':       all_normal,
        'reject_H0':        omnibus['p_value'] < ALPHA,
    })

    pairwise_df = pd.DataFrame()
    if omnibus['reject_H0'] and len(groups) > 2:
        pairwise_df = dunn_pairwise(df_size, 'group', metric)
        pairwise_df['size_label'] = size_label
        pairwise_df['metric']     = metric

    return omnibus, pairwise_df


def print_banner(text: str) -> None:
    line = '=' * 60
    print(f"\n{line}\n  {text}\n{line}")


def main() -> None:
    if not os.path.exists(RAW_CSV):
        sys.exit(f"ERROR: {RAW_CSV} not found. Run scripts/run_experiment.sh first.")

    print_banner("Loading data")
    df = load_data(RAW_CSV)
    print(f"  Rows: {len(df)}")
    print(f"  Patterns: {sorted(df['pattern'].unique())}")
    print(f"  Sizes:    {sorted(df['size_label'].unique())}")

    os.makedirs(OUT_DIR, exist_ok=True)

    # ---- Descriptive statistics ----
    print_banner("Descriptive statistics")
    summary_bw   = compute_summary(df, METRIC)
    summary_lat  = compute_summary(df, METRIC2)
    summary      = pd.merge(
        summary_bw.rename(columns={c: f'{c}_bw'  for c in summary_bw.columns  if c not in ('group', 'size_label', 'n', 'metric')}),
        summary_lat.rename(columns={c: f'{c}_lat' for c in summary_lat.columns if c not in ('group', 'size_label', 'n', 'metric')}),
        on=['group', 'size_label'],
        suffixes=('', '_lat'),
    )
    summary_path = os.path.join(OUT_DIR, 'summary.csv')
    summary_bw.to_csv(summary_path, index=False, float_format='%.6f')
    print(f"  Saved: {summary_path}")

    # Print top performers per size
    for size_label in ['L1', 'L2', 'L3', 'RAM']:
        sub = summary_bw[summary_bw['size_label'] == size_label].sort_values('mean', ascending=False)
        if sub.empty:
            continue
        print(f"\n  {size_label} — top 3 by bandwidth:")
        for _, row in sub.head(3).iterrows():
            print(f"    {row['group']:20s}  mean={row['mean']:.4f} GB/s  "
                  f"CV={row['cv_pct']:.2f}%  CI95=[{row['ci95_low']:.4f}, {row['ci95_high']:.4f}]")

    # ---- Hypothesis tests ----
    print_banner("Hypothesis tests")
    omnibus_rows  = []
    pairwise_dfs  = []

    for size_label in df['size_label'].unique():
        sub = df[df['size_label'] == size_label].copy()
        print(f"\n  [{size_label}]  (n_groups={sub['group'].nunique()})")

        omni, pair = analyse_size(sub, size_label, METRIC)
        omnibus_rows.append(omni)
        if not pair.empty:
            pairwise_dfs.append(pair)

        print(f"    Test:      {omni['test']}")
        print(f"    Statistic: {omni['statistic']:.4f}")
        print(f"    p-value:   {omni['p_value']:.6f}")
        print(f"    H0 rejected (α={ALPHA}): {omni['reject_H0']}")
        if not pair.empty:
            n_sig = pair['significant'].sum()
            print(f"    Post-hoc significant pairs: {n_sig}/{len(pair)}")

    omnibus_df = pd.DataFrame(omnibus_rows)
    omnibus_df.to_csv(os.path.join(OUT_DIR, 'hypothesis_tests.csv'),
                      index=False, float_format='%.8f')

    if pairwise_dfs:
        pd.concat(pairwise_dfs, ignore_index=True).to_csv(
            os.path.join(OUT_DIR, 'pairwise_tests.csv'),
            index=False, float_format='%.8f')

    print_banner("Coefficient of Variation check")
    cv_high = summary_bw[summary_bw['cv_pct'] > 5.0]
    if cv_high.empty:
        print("  All groups: CV < 5% — measurement stable.")
    else:
        print("  WARNING: High variance detected (CV > 5%). "
              "Consider re-running with reduced system load.")
        print(cv_high[['group', 'size_label', 'cv_pct']].to_string(index=False))

    print(f"\nAnalysis complete. Outputs in {OUT_DIR}/")


if __name__ == '__main__':
    main()

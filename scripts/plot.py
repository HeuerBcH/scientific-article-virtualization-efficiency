#!/usr/bin/env python3
"""
plot.py — Generate publication-quality figures for the memory access paper.

Reads:  data/raw/results.csv
Writes: results/figures/fig1_bandwidth_seq_random.{pdf,png}
        results/figures/fig2_stride_bandwidth.{pdf,png}
        results/figures/fig2_stride_latency.{pdf,png}
        results/figures/fig3_block_temporal.{pdf,png}
        results/figures/fig4_boxplot_L3.{pdf,png}
        results/figures/fig5_heatmap_stride.{pdf,png}

Run from project root:
    python3 scripts/plot.py
"""

import os
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

RAW_CSV = os.path.join('data', 'raw', 'results.csv')
FIG_DIR = Path('results') / 'figures'

SIZE_ORDER  = ['L1', 'L2', 'L3', 'RAM']
SIZE_LABELS = {'L1': 'L1 (32 KB)', 'L2': 'L2 (512 KB)',
               'L3': 'L3 (8 MB)',  'RAM': 'RAM (256 MB)'}

PAL = {
    'sequential': '#1565C0',
    'random':     '#B71C1C',
    'stride':     '#E65100',
    'block':      '#2E7D32',
}

plt.rcParams.update({
    'font.family':     'DejaVu Sans',
    'font.size':       10,
    'axes.titlesize':  11,
    'axes.labelsize':  10,
    'legend.fontsize':  9,
    'figure.dpi':      150,
})


def load() -> pd.DataFrame:
    df = pd.read_csv(RAW_CSV)
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


def agg(df: pd.DataFrame, group_cols: list, metric: str):
    """Return mean ± 1.96*SEM (95% CI) per group."""
    g = df.groupby(group_cols)[metric]
    m   = g.mean()
    sem = g.sem()
    return m, 1.96 * sem


def save(fig: plt.Figure, name: str) -> None:
    for ext in ('pdf', 'png'):
        path = FIG_DIR / f'{name}.{ext}'
        fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved {name}")


# ---------------------------------------------------------------------------
# Figure 1 — Sequential vs Random bandwidth across memory levels
# ---------------------------------------------------------------------------
def fig1_seq_vs_random(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))

    x     = np.arange(len(SIZE_ORDER))
    width = 0.35

    for i, pat in enumerate(['sequential', 'random']):
        sub   = df[df['pattern'] == pat]
        means, cis = agg(sub, ['size_label'], 'bandwidth_gbs')
        ys  = [means.get(sl, 0)   for sl in SIZE_ORDER]
        err = [cis.get(sl, 0)     for sl in SIZE_ORDER]
        bars = ax.bar(x + i * width, ys, width,
                      yerr=err, capsize=4,
                      label=pat.capitalize(),
                      color=PAL[pat], alpha=0.85, ecolor='#333333')

    ax.set_xticks(x + width / 2)
    ax.set_xticklabels([SIZE_LABELS[s] for s in SIZE_ORDER])
    ax.set_xlabel('Memory Hierarchy Level (working set size)')
    ax.set_ylabel('Bandwidth (GB/s)')
    ax.set_title('Sequential vs Random Access Bandwidth\nacross Cache Hierarchy Levels')
    ax.legend()
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.grid(axis='y', alpha=0.3, which='both')
    ax.set_ylim(bottom=0)

    save(fig, 'fig1_bandwidth_seq_random')


# ---------------------------------------------------------------------------
# Figure 2 — Stride effect: bandwidth and latency
# ---------------------------------------------------------------------------
def fig2_stride(df: pd.DataFrame) -> None:
    stride_df = df[df['pattern'] == 'stride'].copy()
    strides   = sorted(stride_df['stride'].unique())

    fig, (ax_bw, ax_lat) = plt.subplots(1, 2, figsize=(12, 4.5))
    cmap = plt.get_cmap('tab10')

    for i, size_label in enumerate(SIZE_ORDER):
        sub   = stride_df[stride_df['size_label'] == size_label]
        color = cmap(i)

        bw_mean, bw_ci   = [], []
        lat_mean, lat_ci = [], []
        for s in strides:
            g = sub[sub['stride'] == s]
            bw_mean.append(g['bandwidth_gbs'].mean())
            bw_ci.append(1.96 * g['bandwidth_gbs'].sem())
            lat_mean.append(g['ns_per_element'].mean())
            lat_ci.append(1.96 * g['ns_per_element'].sem())

        label = SIZE_LABELS[size_label]
        ax_bw.errorbar(strides, bw_mean, yerr=bw_ci,
                       marker='o', color=color, label=label, capsize=3)
        ax_lat.errorbar(strides, lat_mean, yerr=lat_ci,
                        marker='o', color=color, label=label, capsize=3)

    for ax in (ax_bw, ax_lat):
        ax.axvline(x=8, color='gray', linestyle='--', alpha=0.7,
                   label='Critical stride\n(8 elem = 64 B = 1 cache line)')
        ax.set_xscale('log', base=2)
        ax.set_xticks(strides)
        ax.set_xticklabels([str(s) for s in strides])
        ax.set_xlabel('Stride (elements)')
        ax.legend(fontsize=8, loc='best')
        ax.grid(alpha=0.3)
        ax.set_ylim(bottom=0)

    ax_bw.set_ylabel('Bandwidth (GB/s)')
    ax_bw.set_title('Stride Access — Bandwidth\n(lower stride = more spatial locality)')

    ax_lat.set_ylabel('Access Latency (ns/element)')
    ax_lat.set_title('Stride Access — Latency\n(higher stride = more cache misses)')

    fig.tight_layout()
    save(fig, 'fig2_stride_effect')


# ---------------------------------------------------------------------------
# Figure 3 — Block (temporal locality) benchmark
# ---------------------------------------------------------------------------
def fig3_block(df: pd.DataFrame) -> None:
    block_df = df[(df['pattern'] == 'block') & (df['size_label'] == 'L3')].copy()
    if block_df.empty:
        print("  fig3: no block data for L3 — skipped")
        return

    seq_l3_bw = df[(df['pattern'] == 'sequential') & (df['size_label'] == 'L3')]['bandwidth_gbs'].mean()

    block_bytes_sorted = sorted(block_df['block_bytes'].unique())
    labels = [f"{int(b // 1024)} KB" for b in block_bytes_sorted]
    means  = [block_df[block_df['block_bytes'] == b]['bandwidth_gbs'].mean()
               for b in block_bytes_sorted]
    cis    = [1.96 * block_df[block_df['block_bytes'] == b]['bandwidth_gbs'].sem()
               for b in block_bytes_sorted]

    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors  = ['#43A047', '#7CB342', '#C0CA33', '#FDD835']
    bars    = ax.bar(labels, means, yerr=cis, capsize=5,
                     color=colors[:len(labels)], alpha=0.85, ecolor='#333333')

    ax.axhline(seq_l3_bw, color=PAL['sequential'], linestyle='--', linewidth=1.5,
               label=f'Sequential L3 ({seq_l3_bw:.2f} GB/s)')

    for bar, val in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f'{val:.2f}', ha='center', va='bottom', fontsize=8)

    ax.set_xlabel('Block Size (bytes)')
    ax.set_ylabel('Effective Bandwidth (GB/s)\n[includes 4× temporal reuse factor]')
    ax.set_title('Temporal Blocking Effect on Bandwidth\n'
                 '(L3-sized array = 8 MB, 4 passes per block)')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(bottom=0)

    save(fig, 'fig3_block_temporal')


# ---------------------------------------------------------------------------
# Figure 4 — Box plots of latency for all patterns (L3 array)
# ---------------------------------------------------------------------------
def fig4_boxplot_l3(df: pd.DataFrame) -> None:
    sub = df[df['size_label'] == 'L3'].copy()

    stride_groups = [f"stride_{s}" for s in [1, 2, 4, 8, 16, 32, 64]]
    block_groups  = [f"block_{int(b // 1024)}KB"
                     for b in sorted(df[df['pattern'] == 'block']['block_bytes'].unique())]
    order = ['sequential', 'random'] + stride_groups + block_groups
    order = [g for g in order if g in sub['group'].unique()]

    data   = [sub[sub['group'] == g]['ns_per_element'].values for g in order]
    data   = [d for d in data if len(d) > 0]
    labels = [g for g in order if len(sub[sub['group'] == g]) > 0]

    if not data:
        print("  fig4: no L3 data — skipped")
        return

    fig, ax = plt.subplots(figsize=(14, 5))
    bp = ax.boxplot(data, labels=labels, patch_artist=True,
                    notch=False, showfliers=True,
                    flierprops={'marker': '.', 'markersize': 4, 'alpha': 0.5})

    colors = (['#90CAF9'] * 2 +
              ['#FFCC80'] * len(stride_groups) +
              ['#A5D6A7'] * len(block_groups))
    colors = colors[:len(bp['boxes'])]
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)

    patches = [
        plt.Rectangle((0, 0), 1, 1, fc='#90CAF9', alpha=0.8, label='Sequential / Random'),
        plt.Rectangle((0, 0), 1, 1, fc='#FFCC80', alpha=0.8, label='Stride'),
        plt.Rectangle((0, 0), 1, 1, fc='#A5D6A7', alpha=0.8, label='Block'),
    ]
    ax.legend(handles=patches, loc='upper left', fontsize=8)

    ax.set_xlabel('Access Pattern')
    ax.set_ylabel('Access Latency (ns/element)')
    ax.set_title('Distribution of Access Latency by Pattern\n(L3-sized array, 8 MB, n=30 runs)')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', alpha=0.3)

    save(fig, 'fig4_boxplot_L3')


# ---------------------------------------------------------------------------
# Figure 5 — Heatmap: bandwidth for all strides × all sizes
# ---------------------------------------------------------------------------
def fig5_heatmap_stride(df: pd.DataFrame) -> None:
    stride_df = df[df['pattern'] == 'stride'].copy()
    strides   = sorted(stride_df['stride'].unique())
    pivot     = stride_df.groupby(['size_label', 'stride'])['bandwidth_gbs'].mean().unstack()
    pivot     = pivot.reindex(index=SIZE_ORDER, columns=strides)

    fig, ax = plt.subplots(figsize=(9, 4))
    im = ax.imshow(pivot.values, aspect='auto', cmap='YlOrRd_r', origin='upper')
    plt.colorbar(im, ax=ax, label='Bandwidth (GB/s)')

    ax.set_xticks(range(len(strides)))
    ax.set_xticklabels([str(s) for s in strides])
    ax.set_yticks(range(len(SIZE_ORDER)))
    ax.set_yticklabels([SIZE_LABELS[s] for s in SIZE_ORDER])
    ax.set_xlabel('Stride (elements)')
    ax.set_ylabel('Memory Level')
    ax.set_title('Stride × Memory Level Bandwidth Heatmap (GB/s)')

    # Annotate cells
    for r, size_label in enumerate(SIZE_ORDER):
        for c, stride in enumerate(strides):
            val = pivot.at[size_label, stride]
            if not np.isnan(val):
                ax.text(c, r, f'{val:.1f}', ha='center', va='center',
                        fontsize=7, color='black')

    save(fig, 'fig5_heatmap_stride')


# ---------------------------------------------------------------------------
def main() -> None:
    if not os.path.exists(RAW_CSV):
        import sys
        sys.exit(f"ERROR: {RAW_CSV} not found. Run scripts/run_experiment.sh first.")

    FIG_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Loading {RAW_CSV}...")
    df = load()
    print(f"  {len(df)} rows\n")

    print("Generating figures...")
    fig1_seq_vs_random(df)
    fig2_stride(df)
    fig3_block(df)
    fig4_boxplot_l3(df)
    fig5_heatmap_stride(df)

    print(f"\nAll figures saved to {FIG_DIR}/")


if __name__ == '__main__':
    main()

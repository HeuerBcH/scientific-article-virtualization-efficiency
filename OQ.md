# O que foi criado

## Código C (src/)
Arquivo	Responsabilidade
benchmarks/common.h	Timer CLOCK_MONOTONIC_RAW, tipo elem_t=double, tamanhos de workload, strides, block configs, declarações
benchmarks/bench_sequential.c	Loop arr[i] sequencial
benchmarks/bench_random.c	Loop arr[idx[i]] com índices pré-gerados
benchmarks/bench_stride.c	Loop arr[i += stride] — one linear pass, n/stride acessos
benchmarks/bench_block.c	Blocos com 4 reps temporais antes de avançar
benchmarks/main.c	Orquestrador: warmup → 30 runs → CSV no stdout
Makefile	-O2 -march=native -fno-tree-vectorize -std=c11
Scripts (scripts/)
Arquivo	Responsabilidade
run_experiment.sh	Compila + taskset -c 0 + executa → data/raw/results.csv
analyze.py	Shapiro-Wilk → ANOVA/Kruskal-Wallis → Dunn pairwise → data/processed/
plot.py	5 figuras para o artigo → results/figures/
Como executar (no WSL2)

# a partir da raiz do projeto
bash scripts/run_experiment.sh

# após o benchmark terminar:
python3 scripts/analyze.py
python3 scripts/plot.py
O run_experiment.sh imprime progresso no stderr e o CSV limpo no stdout. Tempo estimado total: < 5 minutos.
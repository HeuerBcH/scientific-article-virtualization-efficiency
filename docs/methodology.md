# Methodology

## Study Title

Análise Experimental do Impacto de Diferentes Padrões de Acesso à Memória no Desempenho Computacional

---

# Research Question

Como diferentes padrões de acesso à memória influenciam o desempenho computacional em aplicações executadas em sistemas modernos?

---

# Hypotheses

## Null Hypothesis (H0)

Não existe diferença estatisticamente significativa entre os diferentes padrões de acesso à memória quanto ao desempenho observado.

## Alternative Hypothesis (H1)

Existe diferença estatisticamente significativa entre os diferentes padrões de acesso à memória quanto ao desempenho observado.

---

# Experimental Design

## Independent Variable

Padrão de acesso à memória utilizado pelo benchmark.

Os cenários planejados são:

1. Sequential Access
2. Random Access
3. Stride Access
4. Block Access

---

## Dependent Variables

As seguintes métricas serão coletadas:

- Tempo de execução (nanosegundos)
- Throughput (a definir)
- Speedup relativo entre cenários

Observação:

O ambiente WSL2 não permite acesso completo aos contadores de desempenho do processador através do Linux perf.

Por esse motivo, métricas de hardware como cache misses, cache references, branch misses e CPU cycles não serão utilizadas como variáveis dependentes principais.

---

# Experimental Environment

## Hardware

Processador:

- Intel Core i7-12700F
- 10 núcleos físicos
- 20 threads lógicas

Caches:

- L1 Data Cache: 48 KB por núcleo
- L1 Instruction Cache: 32 KB por núcleo
- L2 Cache: 1,25 MB por núcleo
- L3 Cache compartilhada: 25 MB

Memória disponível para a VM WSL2:

- Aproximadamente 16 GB

Topologia NUMA:

- 1 nó NUMA

Detalhes completos disponíveis em:

- experiments/raw/cpuinfo.txt
- experiments/raw/lscpu.txt
- experiments/raw/cache_details.txt
- experiments/raw/numa.txt

---

## Software

Sistema operacional:

- Ubuntu 24.04.2 LTS

Kernel:

- Linux 6.6.114.1-microsoft-standard-WSL2

Compilador:

- GCC 13.3.0

Linguagem principal:

- C

Análise estatística:

- Python 3.12

Bibliotecas planejadas:

- NumPy
- Pandas
- SciPy
- Matplotlib

---

# Benchmark Implementation

Os benchmarks serão implementados em linguagem C.

Todos os cenários executarão operações equivalentes sobre estruturas de dados de mesmo tamanho.

O objetivo é alterar apenas o padrão de acesso à memória, minimizando interferências externas.

---

# Workload Sizes

Tamanhos planejados para os vetores:

PENDENTE.

Os tamanhos deverão ser escolhidos de forma a produzir conjuntos de dados que:

- Caibam integralmente na cache L1
- Excedam a cache L1 mas caibam na cache L2
- Excedam a cache L2 mas caibam na cache L3
- Excedam a cache L3 e utilizem memória principal

A definição final será registrada após a implementação dos benchmarks.

---

# Execution Procedure

Para cada cenário:

1. Compilar utilizando GCC com otimizações definidas.
2. Executar múltiplas repetições independentes.
3. Registrar o tempo de execução.
4. Armazenar os resultados em arquivos CSV.
5. Processar os dados utilizando scripts Python.

---

# Number of Repetitions

PENDENTE.

Valor inicial planejado:

- 30 execuções por combinação de cenário e tamanho de entrada.

A quantidade poderá ser ajustada após experimentos piloto.

---

# Data Collection

Formato previsto:

```csv
pattern,size_bytes,run,time_ns
sequential,32768,1,154321
sequential,32768,2,153998
random,32768,1,482111
```

---

# Há **três informações importantes que ainda precisamos decidir antes de começar a programar os benchmarks**:

1. **Quais tamanhos de vetor serão testados** (essa é a decisão mais importante do projeto).
2. **Qual timer será usado** (`clock_gettime(CLOCK_MONOTONIC_RAW)` é o mais indicado).
3. **Quais flags de compilação serão utilizadas** (`-O2`, `-O3`, etc.).

Eu sugiro que a próxima etapa seja definir os **workload sizes baseados nas caches reais do seu i7-12700F**, porque isso determina todo o desenho experimental do artigo.
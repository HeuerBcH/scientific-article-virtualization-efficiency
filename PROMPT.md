# PROMPT.md

## Contexto Geral

Estou desenvolvendo um artigo científico individual para a disciplina de Infraestrutura de Hardware.

O projeto segue a **Trilha B (trabalho individual aprofundado)** definida pelo professor.

O objetivo deste documento é fornecer contexto completo para que uma IA possa me auxiliar em qualquer etapa do projeto sem perder o histórico das decisões já tomadas.

---

# Requisitos da Disciplina

## Trilha B

* Trabalho individual
* Artigo científico entre 15 e 20 páginas (corpo do texto)
* Cenário experimental aprovado pelo professor
* Hipóteses formais H0 e H1
* Mesmo rigor estatístico da Trilha A
* Mínimo de 5 referências científicas da área
* Repositório Git público contendo:

  * Código-fonte
  * Scripts de execução
  * Dados brutos
  * Dados processados
  * Gráficos
  * Artefatos experimentais

---

# Exigências Metodológicas

O trabalho deve possuir:

* Pergunta de pesquisa
* Revisão bibliográfica
* Metodologia experimental
* Coleta de dados
* Resultados
* Discussão
* Conclusão

Também deve conter:

* Intervalo de confiança de 95%
* Testes de hipótese
* Reprodutibilidade experimental

A análise estatística deve ser cientificamente válida.

---

# Tema Escolhido

## Título Provisório

Análise Experimental do Impacto de Diferentes Padrões de Acesso à Memória no Desempenho Computacional

---

# Pergunta de Pesquisa

Como diferentes padrões de acesso à memória influenciam o desempenho computacional de aplicações que manipulam grandes volumes de dados?

---

# Hipóteses

## H0 (Hipótese Nula)

Não existe diferença estatisticamente significativa entre os diferentes padrões de acesso à memória quanto ao desempenho computacional observado.

## H1 (Hipótese Alternativa)

Existe diferença estatisticamente significativa entre os diferentes padrões de acesso à memória quanto ao desempenho computacional observado.

---

# Motivação

O desempenho de aplicações modernas depende fortemente da forma como os dados são acessados na memória.

Padrões distintos de acesso podem explorar ou prejudicar características arquiteturais dos processadores modernos, como:

* Localidade espacial
* Localidade temporal
* Hierarquia de memória
* Prefetching
* Organização dos dados em memória

Mesmo sem medir diretamente eventos internos da cache, é possível observar experimentalmente seus efeitos por meio do desempenho computacional obtido sob diferentes padrões de acesso.

O objetivo do estudo é quantificar experimentalmente esse impacto.

---

# Objetivos

## Objetivo Geral

Investigar experimentalmente o impacto de diferentes padrões de acesso à memória sobre o desempenho computacional.

## Objetivos Específicos

* Comparar diferentes padrões de acesso à memória.
* Avaliar o impacto do tamanho dos dados sobre o desempenho.
* Identificar diferenças estatisticamente significativas entre os cenários.
* Relacionar os resultados observados com conceitos teóricos de arquitetura de computadores.
* Produzir evidências quantitativas sobre a influência da localidade de referência.

---

# Cenários Experimentais Planejados

## 1. Sequential Access

Acesso sequencial aos elementos de um vetor.

Exemplo:

for(i = 0; i < N; i++)
sum += arr[i];

Objetivo:

Avaliar um cenário com alta localidade espacial.

---

## 2. Random Access

Acesso aleatório aos elementos do vetor.

Exemplo:

sum += arr[rand() % N];

Objetivo:

Avaliar um cenário com baixa localidade espacial.

---

## 3. Stride Access

Acesso utilizando saltos fixos.

Exemplos:

stride = 2

stride = 4

stride = 8

stride = 16

stride = 32

stride = 64

Objetivo:

Investigar como o espaçamento entre acessos influencia o desempenho.

---

## 4. Block Access

Acesso organizado em blocos contíguos de memória.

Objetivo:

Avaliar o efeito da localidade espacial controlada.

---

# Variáveis Experimentais

## Variável Independente

Padrão de acesso à memória.

### Níveis da Variável

* Sequential
* Random
* Stride
* Block

---

## Variável Dependente

Tempo de execução.

---

# Tamanhos de Entrada Planejados

Os experimentos deverão ser executados com diferentes tamanhos de conjuntos de dados.

Tamanhos iniciais planejados:

* 8 KB
* 32 KB
* 48 KB
* 128 KB
* 1 MB
* 2 MB
* 8 MB
* 16 MB
* 25 MB
* 32 MB
* 64 MB
* 128 MB

O objetivo é observar possíveis mudanças de comportamento conforme o volume de dados cresce.

---

# Ferramentas Planejadas

## Linguagens

* C
* Python

## Compilação

* GCC

## Ambiente Experimental

* Ubuntu 24.04 LTS
* WSL2

## Bibliotecas Python

* pandas
* numpy
* scipy
* matplotlib

---

# Coleta de Dados

Pretende-se executar múltiplas repetições por cenário.

Meta inicial:

30 execuções por cenário experimental.

Os resultados serão armazenados em CSV.

Exemplo:

pattern,size_kb,run,time_ns

sequential,1024,1,1045821

random,1024,1,3910042

---

# Análise Estatística Planejada

As análises deverão incluir:

* Média
* Mediana
* Desvio padrão
* Variância
* Intervalo de confiança de 95%

Testes estatísticos possíveis:

* Shapiro-Wilk (normalidade)
* ANOVA
* Kruskal-Wallis

A escolha do teste deverá ser justificada pelos dados coletados.

---

# Estrutura do Repositório

memory-access-patterns-study/

README.md

src/

* sequential_access.c
* random_access.c
* stride_access.c
* block_access.c

scripts/

* run_benchmarks.sh
* process_results.py
* generate_figures.py

data/

* raw/
* processed/

results/

* figures/
* tables/
* statistical_analysis/

paper/

* article.tex
* references.bib

experiments/

* hardware_specs.md
* environment.md

docs/

* methodology.md
* literature_review.md

---

# Ambiente Experimental Conhecido

## Processador

Intel Core i7-12700F

10 núcleos físicos

20 threads lógicas

## Cache

L1 Data Cache: 48 KB

L2 Cache: 1.25 MB

L3 Cache: 25 MB

## Memória

15 GB RAM

## Sistema Operacional

Ubuntu 24.04.2 LTS

Kernel 6.6 WSL2

---

# O que espero da IA

Ao me auxiliar, considere que o objetivo é produzir um artigo científico com rigor acadêmico.

Priorize:

* Metodologias reproduzíveis
* Validade estatística
* Clareza experimental
* Boas práticas de pesquisa
* Reprodutibilidade
* Estrutura compatível com artigos científicos da área de Arquitetura de Computadores e Infraestrutura de Hardware

Ao sugerir análises, considere que o ambiente WSL2 não permite acesso confiável aos contadores de hardware via perf.

Portanto, o foco experimental deve permanecer em métricas diretamente observáveis, especialmente tempo de execução.

Evite sugestões superficiais ou mudanças de tema, exceto quando explicitamente solicitadas.

Considere sempre o tema escolhido, as hipóteses definidas e os requisitos da disciplina.

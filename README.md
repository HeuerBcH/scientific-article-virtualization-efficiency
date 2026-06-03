# Análise Experimental do Impacto de Diferentes Padrões de Acesso à Memória no Desempenho Computacional

## Descrição

Este repositório contém os artefatos experimentais utilizados no desenvolvimento do artigo científico:

> **Análise Experimental do Impacto de Diferentes Padrões de Acesso à Memória no Desempenho Computacional**

O estudo investiga como diferentes padrões de acesso à memória afetam o desempenho computacional de aplicações, analisando a influência da localidade espacial e temporal sobre o tempo de execução em diferentes tamanhos de conjuntos de dados.

A pesquisa busca produzir evidências quantitativas e estatisticamente validadas acerca do impacto dos padrões de acesso à memória no desempenho observado.

---

## Contexto

A memória é um dos principais componentes responsáveis pelo desempenho de sistemas computacionais modernos.

Embora processadores atuais possuam mecanismos sofisticados de otimização, como caches multinível e prefetching, o padrão utilizado para acessar dados pode influenciar significativamente a eficiência da execução de programas.

Este trabalho busca avaliar experimentalmente esse comportamento por meio de benchmarks controlados e reprodutíveis.

---

## Pergunta de Pesquisa

**Como diferentes padrões de acesso à memória influenciam o desempenho computacional de aplicações que manipulam grandes volumes de dados?**

---

## Hipóteses

### Hipótese Nula (H0)

Não existe diferença estatisticamente significativa entre os diferentes padrões de acesso à memória quanto ao desempenho computacional observado.

### Hipótese Alternativa (H1)

Existe diferença estatisticamente significativa entre os diferentes padrões de acesso à memória quanto ao desempenho computacional observado.

---

## Objetivo Geral

Investigar experimentalmente a influência de diferentes padrões de acesso à memória sobre o desempenho computacional.

---

## Objetivos Específicos

* Implementar benchmarks representando diferentes padrões de acesso à memória.
* Avaliar o impacto desses padrões sobre o tempo de execução.
* Comparar o comportamento observado em diferentes tamanhos de entrada.
* Produzir análises estatísticas dos resultados obtidos.
* Relacionar os resultados experimentais com conceitos de arquitetura de computadores e hierarquia de memória.

---

## Cenários Experimentais

### Sequential Access

Acesso sequencial aos elementos de uma estrutura de dados.

Características:

* Alta localidade espacial
* Acesso previsível
* Comportamento esperado de maior eficiência

---

### Random Access

Acesso aleatório aos elementos da estrutura.

Características:

* Baixa localidade espacial
* Baixa previsibilidade
* Potencial impacto negativo no desempenho

---

### Stride Access

Acesso utilizando saltos fixos entre elementos consecutivos.

Exemplos:

* Stride = 2
* Stride = 4
* Stride = 8
* Stride = 16
* Stride = 32
* Stride = 64

Objetivo:

Avaliar como o espaçamento entre acessos influencia o desempenho.

---

### Block Access

Acesso organizado em blocos contíguos de memória.

Objetivo:

Avaliar os efeitos da exploração controlada da localidade espacial.

---

## Tamanhos de Entrada

Os experimentos serão executados com diferentes tamanhos de conjuntos de dados para avaliar possíveis mudanças de comportamento conforme o volume de dados cresce.

Tamanhos planejados:

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

---

## Variáveis do Estudo

### Variável Independente

Padrão de acesso à memória.

### Variável Dependente

Tempo de execução.

---

## Métricas Coletadas

### Métrica Principal

* Tempo de execução (nanosegundos ou microssegundos)

### Métricas Estatísticas

* Média
* Mediana
* Desvio padrão
* Variância
* Intervalo de confiança de 95%
* Ganho/perda relativa de desempenho

---

## Metodologia Estatística

Cada cenário experimental será executado múltiplas vezes para reduzir o efeito de variações do sistema operacional e do ambiente de execução.

Planejamento inicial:

* 30 repetições por cenário

Análises previstas:

* Teste de normalidade (Shapiro-Wilk)
* ANOVA (quando aplicável)
* Kruskal-Wallis (quando aplicável)
* Intervalo de confiança de 95%

---

## Ferramentas Utilizadas

### Desenvolvimento

* Linguagem C
* GCC

### Ambiente Experimental

* Ubuntu 24.04 LTS
* WSL2

### Processamento e Análise de Dados

* Python 3
* NumPy
* Pandas
* SciPy
* Matplotlib

---

## Estrutura do Repositório

### src/

Implementações dos benchmarks utilizados nos experimentos.

### scripts/

Scripts responsáveis pela automação da execução dos testes, coleta dos dados e geração de resultados.

### data/raw/

Dados brutos produzidos durante os experimentos.

### data/processed/

Dados tratados e preparados para análise estatística.

### results/

Resultados finais da pesquisa.

Contém:

* Gráficos
* Tabelas
* Análises estatísticas

### experiments/

Informações sobre hardware, sistema operacional e ambiente experimental.

### docs/

Materiais auxiliares:

* Planejamento
* Metodologia
* Revisão bibliográfica

### paper/

Arquivos relacionados ao artigo científico.

---

## Reprodutibilidade

Todos os experimentos podem ser reproduzidos executando:

```bash
./scripts/run_benchmarks.sh
```

Os dados podem ser processados através de:

```bash
python scripts/process_results.py
```

Os gráficos podem ser gerados através de:

```bash
python scripts/generate_figures.py
```

---

## Licença

Este projeto é disponibilizado exclusivamente para fins acadêmicos e científicos.

---

## Autor

Bernardo Heuer

Disciplina de Infraestrutura de Hardware

2026

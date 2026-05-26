# Eficiência de Virtualização: Bare-metal vs Docker vs VirtualBox

## Descrição

Este repositório contém os experimentos, scripts, dados e análises estatísticas utilizados no artigo científico desenvolvido para a disciplina de Infraestrutura de Hardware.

O trabalho investiga o impacto da virtualização baseada em containers e hipervisores sobre o desempenho computacional em diferentes tipos de carga de trabalho, comparando:

- Execução Bare-metal
- Containers Docker
- Máquinas Virtuais VirtualBox

O objetivo é avaliar o overhead introduzido por cada tecnologia em cenários CPU-bound, memory-bound e I/O-bound.

---

# Pergunta de Pesquisa

> Qual o impacto da virtualização baseada em containers e hipervisores no desempenho computacional de cargas CPU-bound, memory-bound e I/O-bound em comparação à execução bare-metal?

---

# Objetivos

## Objetivo Geral

Comparar o desempenho computacional entre ambientes bare-metal, Docker e VirtualBox utilizando benchmarks padronizados.

## Objetivos Específicos

- Medir overhead de virtualização
- Avaliar throughput e latência
- Comparar desempenho de CPU, memória e disco
- Aplicar análise estatística sobre os resultados
- Identificar diferenças estatisticamente significativas

---

# Ambiente Experimental

## Hardware

Preencher posteriormente:

- Processador:
- Quantidade de núcleos:
- Threads:
- Memória RAM:
- Disco:
- Arquitetura:

---

## Software

- Sistema Operacional:
- Kernel Linux:
- Docker:
- VirtualBox:
- Python:
- GCC:

---

# Ferramentas Utilizadas

## CPU

- stress-ng
- perf
- taskset

### Exemplos

```bash
stress-ng --cpu 4 --timeout 60s

perf stat -e cycles,instructions ./programa

taskset -c 0,2 ./programa
```

---

## Memória

- sysbench
- vmstat

### Exemplos

```bash
sysbench memory --memory-block-size=1K run

sysbench memory --memory-access-mode=rnd run

vmstat 1 30
```

---

## Entrada e Saída (I/O)

- fio
- iostat

### Exemplos

```bash
fio --name=rand --rw=randread --iodepth=32

fio --name=seq --rw=write --bs=1M

iostat -x 1
```

---

# Metodologia Experimental

Executados nos seguintes ambientes:

- Bare-metal
- Docker
- VirtualBox

Executados 30 vezes para:

- reduzir variabilidade experimental;
- aumentar confiabilidade dos resultados;
- permitir análise estatística;
- calcular intervalo de confiança de 95%;
- aplicar testes de hipótese.

---

# Métricas Avaliadas

- Tempo de execução
- Throughput
- Latência
- Uso de CPU
- Overhead
- IPC (Instructions Per Cycle)
- Context Switches
- Utilização de memória
- IOPS
- Bandwidth

---

# Controle Experimental

Para reduzir interferências externas:

- Afinidade de CPU será controlada via `taskset`
- Governor da CPU será fixado
- Processos paralelos serão minimizados
- Todos os testes utilizarão a mesma configuração de hardware
- Os ambientes virtualizados terão recursos equivalentes

---

# Análise Estatística

Realizada em Python utilizando:

- NumPy
- SciPy
- Pandas
- Matplotlib

---

# Geração de Gráficos

Os gráficos incluirão:

- Boxplots
- Barras com erro
- Histogramas
- Distribuições de latência

---

# Reprodutibilidade

Todos os scripts, dados brutos e resultados utilizados no artigo estarão disponíveis neste repositório para garantir reprodutibilidade experimental.

---

# Artigo Científico

O artigo será submetido para:

- WSCAD 2026

Utilizando:

- Template oficial da SBC

---

# Integrantes

Bernardo Heuer
Eduardo Roma

---

# Licença

...
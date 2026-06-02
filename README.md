# Impacto do WSL2 no Desempenho de Hardware: Uma Análise Experimental

## Autor

Bernardo Carneiro Heuer Guimarães

## Disciplina

Infraestrutura de Hardware

Professor: Ronierison Maciel

CESAR School – 2026

---

## Resumo

O Windows Subsystem for Linux 2 (WSL2) tornou-se uma das principais soluções para execução de aplicações Linux em ambientes Windows. Apesar de sua ampla adoção em desenvolvimento de software, ainda existem dúvidas sobre o impacto da camada de virtualização em medições de desempenho de hardware.

Este trabalho investiga os efeitos do WSL2 sobre métricas de CPU, memória e armazenamento por meio de experimentos controlados executados em ambiente nativo e virtualizado.

Os resultados serão analisados utilizando métodos estatísticos, incluindo intervalos de confiança de 95% e testes de hipótese, buscando determinar se as diferenças observadas são estatisticamente significativas.

---

## Pergunta de Pesquisa

O ambiente WSL2 produz resultados de desempenho estatisticamente equivalentes aos obtidos em execução nativa?

---

## Hipóteses

### Hipótese Nula (H0)

Não existe diferença estatisticamente significativa entre os resultados de desempenho obtidos em ambiente WSL2 e em ambiente nativo.

### Hipótese Alternativa (H1)

Existe diferença estatisticamente significativa entre os resultados de desempenho obtidos em ambiente WSL2 e em ambiente nativo.

---

## Objetivos

### Objetivo Geral

Avaliar o impacto da virtualização do WSL2 em métricas de desempenho de hardware.

### Objetivos Específicos

- Comparar desempenho de CPU entre WSL2 e ambiente nativo.
- Comparar largura de banda de memória.
- Comparar desempenho de armazenamento.
- Avaliar o comportamento de interrupções e virtualização de dispositivos.
- Quantificar o overhead introduzido pelo WSL2.
- Verificar a significância estatística das diferenças observadas.

---

## Ambiente Experimental

### Hardware

- CPU: Intel Core i7-12700F
- RAM: 16 GB DDR4
- Armazenamento: SSD NVMe 1 TB

### Sistemas Operacionais

#### Ambiente Nativo

- Windows 11 Pro

#### Ambiente Virtualizado

- Ubuntu Linux executado via WSL2

---

## Ferramentas Utilizadas

### CPU

- stress-ng
- sysbench
- perf

### Memória

- sysbench memory
- mbw

### Armazenamento

- fio

### Monitoramento

- vmstat
- iostat
- lscpu
- free
- lspci

### Análise Estatística

- Python
- NumPy
- SciPy
- Pandas
- Matplotlib

---

## Metodologia

Cada benchmark será executado no ambiente nativo e no ambiente WSL2.

Para garantir rigor estatístico:

- 30 repetições por condição experimental
- descarte das execuções de warm-up
- coleta automatizada dos resultados
- cálculo de média
- cálculo de desvio padrão
- cálculo de intervalo de confiança de 95%
- aplicação de teste t de Student ou Wilcoxon

---

## Experimentos

### Experimento 1 – CPU

Objetivo:

Comparar capacidade de processamento entre os ambientes.

Métricas:

- tempo de execução
- throughput
- utilização dos núcleos

Ferramentas:

- stress-ng
- sysbench CPU

---

### Experimento 2 – Memória

Objetivo:

Avaliar largura de banda e acesso à memória.

Métricas:

- largura de banda (MB/s)
- latência relativa

Ferramentas:

- mbw
- sysbench memory

---

### Experimento 3 – Armazenamento

Objetivo:

Comparar desempenho de I/O.

Métricas:

- throughput
- IOPS
- latência

Ferramentas:

- fio

---

### Experimento 4 – Benchmark Integrado

Objetivo:

Avaliar comportamento do sistema sob carga mista.

Métricas:

- CPU
- memória
- I/O

Ferramentas:

- workload personalizado

---

## Resultados Esperados

Espera-se que:

- CPU apresente baixo overhead.
- Memória apresente impacto moderado.
- Armazenamento apresente maior degradação.
- Alguns benchmarks apresentem diferenças estatisticamente significativas entre os ambientes.

---

## Ameaças à Validade

- Influência do escalonador do Windows.
- Processos em segundo plano.
- Variações térmicas da CPU.
- Limitações inerentes ao Hyper-V.
- Diferenças entre sistema de arquivos virtualizado e acesso nativo.

---

## Licença

Projeto acadêmico desenvolvido para a disciplina de Infraestrutura de Hardware da CESAR School.

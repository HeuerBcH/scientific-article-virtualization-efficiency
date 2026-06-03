# Especificação do Hardware Experimental

## Objetivo

Este documento descreve a plataforma de hardware utilizada para execução dos experimentos apresentados no estudo:

**"Análise Experimental do Impacto de Diferentes Padrões de Acesso à Memória no Desempenho Computacional"**

---

# Processador

Modelo:

Intel Core i7-12700F (12ª Geração)

Fabricante:

Intel Corporation

Microarquitetura:

Alder Lake

Identificação:

* CPU Family: 6
* Model: 151
* Stepping: 2

Configuração observada pelo sistema experimental:

* 10 núcleos lógicos visíveis
* 20 threads lógicas
* Hyper-Threading habilitado

---

# Hierarquia de Cache

## Cache L1

### L1 Data Cache (L1D)

* Tamanho por núcleo: 48 KB
* Associatividade: não reportada
* Line Size: 64 bytes

### L1 Instruction Cache (L1I)

* Tamanho por núcleo: 32 KB
* Line Size: 64 bytes

---

## Cache L2

* Tamanho por núcleo: 1.25 MB
* Tipo: Unified
* Line Size: 64 bytes

---

## Cache L3

* Tamanho total: 25 MB
* Compartilhada entre os núcleos
* Tipo: Unified
* Line Size: 64 bytes

---

# Topologia

## Socket

* 1 socket físico

## NUMA

Configuração NUMA observada:

* 1 nó NUMA

Memória disponível:

* Aproximadamente 15.9 GB

Distância NUMA:

Node 0 → Node 0 = 10

Como existe apenas um nó NUMA, efeitos de acesso remoto à memória não são esperados.

---

# Memória Principal

Memória disponível para o ambiente experimental:

* Aproximadamente 16 GB

---

# Características Relevantes

* Cache line de 64 bytes
* Suporte a SSE, SSE2, SSE4.1, SSE4.2
* Suporte a AVX e AVX2
* Suporte a FMA
* Hyper-Threading habilitado

Essas características podem influenciar diretamente o comportamento observado nos experimentos de acesso à memória.

---

# Limitações

Os experimentos são executados em ambiente virtualizado WSL2.

Consequentemente:

* Não há acesso confiável aos contadores de hardware de desempenho.
* Métricas como cache misses, cache references e branch misses não podem ser coletadas.
* A análise será baseada principalmente em tempo de execução e throughput observado.

Essa limitação é discutida na seção de ameaças à validade do estudo.

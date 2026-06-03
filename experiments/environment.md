# Ambiente Experimental

## Sistema Operacional

Distribuição:

Ubuntu 24.04.2 LTS

Codename:

Noble Numbat

Kernel:

Linux 6.6.114.1-microsoft-standard-WSL2

Arquitetura:

x86_64

---

# Ambiente de Execução

Os experimentos são executados dentro do Windows Subsystem for Linux 2 (WSL2).

Características observadas:

* Hypervisor: Microsoft
* Tipo de virtualização: Full Virtualization
* Virtualização Intel VT-x habilitada

---

# Compilador

GCC:

13.3.0

Comando utilizado para verificação:

gcc --version

---

# Python

Versão:

Python 3.12.3

---

# Temporização

Relógio utilizado:

clock_gettime()

Resolução observada:

1 ns

---

# Estado do Sistema

Antes da execução dos experimentos recomenda-se:

* Fechar aplicações desnecessárias.
* Encerrar tarefas de background intensivas.
* Executar os testes em condição ociosa.

Medições preliminares indicaram:

* Uso de CPU próximo de 0%.
* Sistema predominantemente em estado idle (>99%).

---

# Configuração Experimental

Para minimizar interferências externas:

* Cada cenário será executado múltiplas vezes.
* As execuções serão realizadas sob as mesmas condições de software.
* Os resultados serão armazenados em formato CSV.
* Serão calculados média, desvio padrão e intervalo de confiança de 95%.

---

# Limitações do Ambiente

Por utilizar WSL2:

* Não há acesso direto aos PMCs (Performance Monitoring Counters).
* Ferramentas como perf não podem coletar eventos reais de hardware.
* Resultados relacionados à hierarquia de cache serão inferidos indiretamente através do tempo de execução.

Portanto, o estudo avalia o impacto dos padrões de acesso à memória sobre o desempenho observado, e não métricas internas da microarquitetura.

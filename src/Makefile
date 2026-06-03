CC      := gcc
# -O2           : standard production optimization (no SIMD auto-vectorization at this level by default
#                 on some GCC versions, but we add the explicit flag below for certainty)
# -march=native : enables Alder Lake–specific instructions without enabling AVX-512 vectorized loops
# -fno-tree-vectorize : explicitly prevents auto-vectorization so the benchmark measures scalar
#                 memory hierarchy behavior, not SIMD throughput (documented in methodology)
# -std=c11      : guarantees clock_gettime and stdint types
# -Wall -Wextra : catch any issues
CFLAGS  := -O2 -march=native -fno-tree-vectorize -std=c11 -Wall -Wextra
LDFLAGS := -lm

BENCH_DIR := benchmarks
SRCS := $(BENCH_DIR)/main.c          \
        $(BENCH_DIR)/bench_sequential.c \
        $(BENCH_DIR)/bench_random.c     \
        $(BENCH_DIR)/bench_stride.c     \
        $(BENCH_DIR)/bench_block.c

TARGET := benchmark

.PHONY: all clean check-env

all: check-env $(TARGET)

check-env:
	@echo "Compiler: $$($(CC) --version | head -1)"
	@echo "CFLAGS:   $(CFLAGS)"

$(TARGET): $(SRCS) $(BENCH_DIR)/common.h
	$(CC) $(CFLAGS) -o $@ $(SRCS) $(LDFLAGS)
	@echo "Built: $(TARGET)"

clean:
	rm -f $(TARGET)

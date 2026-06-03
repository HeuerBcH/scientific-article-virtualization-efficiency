#ifndef COMMON_H
#define COMMON_H

#define _POSIX_C_SOURCE 200809L

#include <stdint.h>
#include <stddef.h>
#include <time.h>

/* Element type: 8 bytes → 8 elements per 64-byte cache line (i7-12700F) */
typedef double elem_t;
#define ELEM_SIZE ((size_t)sizeof(elem_t))

/* High-resolution monotonic timer — not affected by NTP adjustments */
static inline uint64_t now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC_RAW, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ULL + (uint64_t)ts.tv_nsec;
}

/*
 * Workload sizes calibrated for Intel Core i7-12700F cache hierarchy:
 *   L1D = 48 KB/core | L2 = 1280 KB/core | L3 = 25 MB shared
 *
 * Targets are set *below* each cache limit to ensure the working set
 * fits cleanly within the intended level with margin.
 *
 * inner: repetitions per timed run — scaled so wall time stays ~10–200 ms,
 * keeping timer overhead (< 100 ns) negligible relative to measurement.
 */
#define N_SIZES 4
typedef struct {
    const char *label;
    size_t      bytes;
    size_t      inner;
} workload_t;

static const workload_t WORKLOADS[N_SIZES] = {
    { "L1",    32ULL * 1024,              50000 },  /*  32 KB  — fits in L1D (48 KB)    */
    { "L2",   512ULL * 1024,               1000 },  /* 512 KB  — fits in L2  (1280 KB)  */
    { "L3",     8ULL * 1024 * 1024,          10 },  /*   8 MB  — fits in L3  (25 MB)    */
    { "RAM",  256ULL * 1024 * 1024,           1 },  /* 256 MB  — exceeds L3             */
};

/*
 * Stride values in elements (not bytes).
 * Critical stride for elem_t (8 bytes) is 8 → each access lands on a different
 * cache line (64 bytes / 8 bytes = 8 elements per line).
 * Strides below 8: spatial locality (multiple hits per cache line load).
 * Strides >= 8: one or zero cache line reuses per access.
 */
#define N_STRIDES 7
static const size_t STRIDES[N_STRIDES] = { 1, 2, 4, 8, 16, 32, 64 };

/*
 * Block (temporal locality) benchmark — L3-sized array only.
 * The array is traversed in contiguous blocks of BLOCK_BYTES bytes.
 * Within each block, BLOCK_TEMPORAL_REPS passes are made before advancing,
 * simulating temporal reuse. If BLOCK_BYTES fits in L1, reps 2..N are L1 hits.
 */
#define N_BLOCK_SIZES 4
static const size_t BLOCK_BYTES[N_BLOCK_SIZES] = {
    2ULL  * 1024,         /*  2 KB  — fits in L1D                  */
    32ULL * 1024,         /* 32 KB  — borderline L1D (L1D = 48 KB) */
    512ULL * 1024,        /* 512 KB — fits in L2                   */
    8ULL  * 1024 * 1024,  /*  8 MB  — full L3 array (no L1 reuse)  */
};
#define BLOCK_TEMPORAL_REPS 4

/* Benchmark function declarations (defined in separate translation units
 * to prevent the compiler from inlining and optimizing across the timer) */
double bench_sequential(const elem_t *arr, size_t n, size_t inner_iters);
double bench_random    (const elem_t *arr, const uint32_t *idx,
                        size_t n, size_t inner_iters);
double bench_stride    (const elem_t *arr, size_t n,
                        size_t stride, size_t inner_iters);
double bench_block     (const elem_t *arr, size_t n,
                        size_t block_elems, size_t temporal_reps,
                        size_t inner_iters);

#endif /* COMMON_H */

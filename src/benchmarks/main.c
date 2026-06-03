#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <inttypes.h>
#include "common.h"

#define N_RUNS    30   /* independent timed runs per (pattern, size) combination */
#define N_WARMUP   3   /* discarded runs before measurement begins              */

/*
 * Volatile sink: the return value of every benchmark function is added here.
 * Because g_sink is volatile, the compiler must perform the store, which in
 * turn forces all computations feeding into the return value to execute.
 * Without this, an optimizing compiler could legally remove the entire loop.
 */
volatile double g_sink = 0.0;

/* Fill array with deterministic non-zero values to avoid branch-prediction
 * artifacts from zero-heavy data and to prevent constant-folding. */
static void init_array(elem_t *arr, size_t n) {
    for (size_t i = 0; i < n; i++) {
        arr[i] = (elem_t)(1.0 + (double)(i % 1024) * 0.001);
    }
}

/*
 * Linear congruential generator (Knuth) for index generation.
 * Faster than rand() and avoids global-state contention.
 * Bias from modulo is negligible for this purpose.
 */
static void gen_random_indices(uint32_t *idx, size_t n) {
    uint32_t state = 0xDEADBEEFu;
    uint32_t n32   = (uint32_t)n;
    for (size_t i = 0; i < n; i++) {
        state = state * 1664525u + 1013904223u;
        idx[i] = state % n32;
    }
}

/*
 * Emit one CSV data row.
 *
 * Bandwidth formula:
 *   bandwidth_gbs = bytes_per_pass / time_per_pass_ns
 *
 * Because 1 GB = 10^9 bytes and 1 ns = 10^{-9} s:
 *   bytes / ns = bytes * 10^9 / (10^9 * s) = GB/s  ✓
 *
 * ns_per_element = time_per_pass_ns / elements_accessed_per_pass
 *   — measures per-access latency, useful for stride/random comparison.
 */
static void emit_row(
        const char *pattern,
        size_t      stride_val,
        size_t      block_bytes_val,
        const char *size_label,
        size_t      size_bytes,
        int         run,
        size_t      inner_iters,
        uint64_t    total_time_ns,
        size_t      elements_per_pass)
{
    double time_per_pass_ns   = (double)total_time_ns / (double)inner_iters;
    size_t bytes_per_pass     = elements_per_pass * ELEM_SIZE;
    double bandwidth_gbs      = (double)bytes_per_pass / time_per_pass_ns;
    double ns_per_element     = time_per_pass_ns / (double)elements_per_pass;

    printf("%s,%zu,%zu,%s,%zu,%d,%zu,%" PRIu64 ",%.3f,%zu,%zu,%.6f,%.4f\n",
           pattern,
           stride_val,
           block_bytes_val,
           size_label,
           size_bytes,
           run,
           inner_iters,
           total_time_ns,
           time_per_pass_ns,
           elements_per_pass,
           bytes_per_pass,
           bandwidth_gbs,
           ns_per_element);
}

int main(void) {
    /* CSV header — column semantics documented inline */
    puts("pattern,"          /* access pattern name                         */
         "stride,"           /* stride in elements (1 = sequential/random)  */
         "block_bytes,"      /* block size in bytes (0 = not a block bench) */
         "size_label,"       /* cache level target: L1/L2/L3/RAM            */
         "size_bytes,"       /* array size in bytes                         */
         "run,"              /* run index 1..N_RUNS                         */
         "inner_iters,"      /* repetitions batched per timed measurement   */
         "total_time_ns,"    /* wall time for all inner_iters passes (ns)   */
         "time_per_pass_ns," /* total_time_ns / inner_iters                 */
         "elements_accessed,"/* elements touched per pass                   */
         "bytes_accessed,"   /* elements_accessed * 8                       */
         "bandwidth_gbs,"    /* bytes_accessed / time_per_pass_ns (GB/s)    */
         "ns_per_element");  /* time_per_pass_ns / elements_accessed        */

    /* ------------------------------------------------------------------ */
    /* Sequential, Random, and Stride — run across all four workload sizes */
    /* ------------------------------------------------------------------ */
    for (int wi = 0; wi < N_SIZES; wi++) {
        const workload_t *w = &WORKLOADS[wi];
        size_t n     = w->bytes / ELEM_SIZE;
        size_t inner = w->inner;

        elem_t   *arr = (elem_t *)  malloc(w->bytes);
        uint32_t *idx = (uint32_t *)malloc(n * sizeof(uint32_t));
        if (!arr || !idx) {
            fprintf(stderr, "Out of memory allocating workload %s\n", w->label);
            exit(EXIT_FAILURE);
        }
        init_array(arr, n);
        gen_random_indices(idx, n);

        fprintf(stderr, "Workload %s (%zu MB, n=%zu, inner=%zu)\n",
                w->label, w->bytes / (1024 * 1024) + 1, n, inner);

        /* -- Sequential -- */
        fprintf(stderr, "  sequential...\n");
        for (int r = 0; r < N_WARMUP; r++) g_sink += bench_sequential(arr, n, 1);
        for (int r = 1; r <= N_RUNS; r++) {
            uint64_t t0 = now_ns();
            g_sink += bench_sequential(arr, n, inner);
            uint64_t t1 = now_ns();
            emit_row("sequential", 1, 0, w->label, w->bytes, r, inner, t1 - t0, n);
        }

        /* -- Random -- */
        fprintf(stderr, "  random...\n");
        for (int r = 0; r < N_WARMUP; r++) g_sink += bench_random(arr, idx, n, 1);
        for (int r = 1; r <= N_RUNS; r++) {
            uint64_t t0 = now_ns();
            g_sink += bench_random(arr, idx, n, inner);
            uint64_t t1 = now_ns();
            emit_row("random", 1, 0, w->label, w->bytes, r, inner, t1 - t0, n);
        }

        /* -- Stride (all stride values) -- */
        for (int si = 0; si < N_STRIDES; si++) {
            size_t stride      = STRIDES[si];
            size_t n_accesses  = n / stride;
            if (n_accesses == 0) continue;

            fprintf(stderr, "  stride=%zu (%zu accesses/pass)...\n",
                    stride, n_accesses);

            for (int r = 0; r < N_WARMUP; r++)
                g_sink += bench_stride(arr, n, stride, 1);
            for (int r = 1; r <= N_RUNS; r++) {
                uint64_t t0 = now_ns();
                g_sink += bench_stride(arr, n, stride, inner);
                uint64_t t1 = now_ns();
                emit_row("stride", stride, 0, w->label, w->bytes,
                         r, inner, t1 - t0, n_accesses);
            }
        }

        free(idx);
        free(arr);
    }

    /* ------------------------------------------------------------------ */
    /* Block (temporal locality) — L3-sized array, varying block sizes     */
    /* ------------------------------------------------------------------ */
    {
        const workload_t *w = &WORKLOADS[2];  /* L3: 8 MB */
        size_t n     = w->bytes / ELEM_SIZE;
        size_t inner = 5;  /* reduced: block benchmark does 4× more work per pass */

        elem_t *arr = (elem_t *)malloc(w->bytes);
        if (!arr) {
            fprintf(stderr, "Out of memory allocating block array\n");
            exit(EXIT_FAILURE);
        }
        init_array(arr, n);

        fprintf(stderr, "Block benchmark (%s array, temporal_reps=%d)\n",
                w->label, BLOCK_TEMPORAL_REPS);

        for (int bi = 0; bi < N_BLOCK_SIZES; bi++) {
            size_t block_bytes = BLOCK_BYTES[bi];
            size_t block_elems = block_bytes / ELEM_SIZE;
            if (block_elems == 0) block_elems = 1;

            /* Total elements touched per pass: all n elements, temporal_reps times */
            size_t elements_per_pass = n * BLOCK_TEMPORAL_REPS;

            fprintf(stderr, "  block_bytes=%zu KB...\n", block_bytes / 1024);

            for (int r = 0; r < N_WARMUP; r++)
                g_sink += bench_block(arr, n, block_elems, BLOCK_TEMPORAL_REPS, 1);
            for (int r = 1; r <= N_RUNS; r++) {
                uint64_t t0 = now_ns();
                g_sink += bench_block(arr, n, block_elems, BLOCK_TEMPORAL_REPS, inner);
                uint64_t t1 = now_ns();
                emit_row("block", 1, block_bytes, w->label, w->bytes,
                         r, inner, t1 - t0, elements_per_pass);
            }
        }
        free(arr);
    }

    /* Print checksum to stderr so it doesn't contaminate CSV stdout */
    fprintf(stderr, "\nchecksum (ignore value, existence proves no dead-code elimination): %f\n",
            g_sink);
    return EXIT_SUCCESS;
}

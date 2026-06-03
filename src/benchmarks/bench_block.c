#define _POSIX_C_SOURCE 200809L
#include "common.h"

/*
 * Block (temporal locality) access.
 *
 * The array is divided into contiguous blocks of block_elems elements.
 * For each block, temporal_reps passes are made before moving to the
 * next block. This models cache-aware (blocked) algorithms.
 *
 * Behavior by block size relative to cache levels (elem_t = 8 bytes):
 *   block_bytes <  L1 : after the 1st rep, all subsequent reps are L1 hits
 *   block_bytes <  L2 : reps after 1st may hit L2 (data stays in L2)
 *   block_bytes <  L3 : reps benefit from L3 reuse
 *   block_bytes >= L3 : equivalent to temporal_reps sequential scans (no reuse)
 *
 * Total elements accessed per pass = n * temporal_reps.
 * Effective bandwidth = (n * temporal_reps * ELEM_SIZE) / time_per_pass.
 *
 * A small block that fits in L1 will achieve near L1 bandwidth even when
 * the total array is L3- or RAM-sized, demonstrating the benefit of blocking.
 */
double bench_block(const elem_t *arr, size_t n,
                   size_t block_elems, size_t temporal_reps,
                   size_t inner_iters) {
    double total = 0.0;
    for (size_t iter = 0; iter < inner_iters; iter++) {
        double s = 0.0;
        for (size_t bstart = 0; bstart < n; bstart += block_elems) {
            size_t bend = bstart + block_elems;
            if (bend > n) bend = n;
            for (size_t rep = 0; rep < temporal_reps; rep++) {
                for (size_t i = bstart; i < bend; i++) {
                    s += arr[i];
                }
            }
        }
        total += s;
    }
    return total;
}

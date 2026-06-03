#define _POSIX_C_SOURCE 200809L
#include "common.h"
#include <stdint.h>

/*
 * Random access: arr[idx[0]], arr[idx[1]], ..., arr[idx[n-1]].
 *
 * idx is a pre-generated array of random indices into arr.
 * Pre-generation outside the timed region avoids measuring rand() overhead.
 *
 * The idx array itself is accessed sequentially, which the hardware
 * prefetcher can handle. The bottleneck is the unpredictable load of
 * arr[idx[i]], which defeats the hardware prefetcher for arr.
 *
 * This isolates the effect of spatial locality loss: the working set
 * size is the same as sequential, but cache utilization collapses.
 */
double bench_random(const elem_t *arr, const uint32_t *idx,
                    size_t n, size_t inner_iters) {
    double total = 0.0;
    for (size_t iter = 0; iter < inner_iters; iter++) {
        double s = 0.0;
        for (size_t i = 0; i < n; i++) {
            s += arr[idx[i]];
        }
        total += s;
    }
    return total;
}

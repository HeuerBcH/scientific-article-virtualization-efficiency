#define _POSIX_C_SOURCE 200809L
#include "common.h"

/*
 * Stride access: arr[0], arr[stride], arr[2*stride], ..., arr[k*stride]
 * where k = (n / stride) - 1.
 *
 * One pass makes exactly (n / stride) accesses over the full array range.
 * The number of accesses decreases as stride grows, but the spatial range
 * covered (n * ELEM_SIZE bytes) remains constant.
 *
 * Key thresholds for elem_t = double (8 bytes):
 *   stride < 8 : multiple elements loaded per cache line (spatial locality)
 *   stride = 8 : exactly one element per cache line (critical stride)
 *   stride > 8 : cache lines are wasted; prefetcher may still help for
 *                small strides but TLB pressure grows for stride >= 64
 *
 * The caller computes (n / stride) to report actual elements accessed.
 */
double bench_stride(const elem_t *arr, size_t n,
                    size_t stride, size_t inner_iters) {
    double total = 0.0;
    for (size_t iter = 0; iter < inner_iters; iter++) {
        double s = 0.0;
        for (size_t i = 0; i < n; i += stride) {
            s += arr[i];
        }
        total += s;
    }
    return total;
}

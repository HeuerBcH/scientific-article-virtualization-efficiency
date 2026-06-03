#define _POSIX_C_SOURCE 200809L
#include "common.h"

/*
 * Sequential access: arr[0], arr[1], ..., arr[n-1].
 *
 * Compiled in a separate translation unit so the compiler cannot inline
 * this function into main() and eliminate the loop as dead code.
 * The return value (sum) is consumed by the caller via a volatile sink,
 * which forces the entire computation to execute.
 *
 * inner_iters consecutive passes are timed together to reduce relative
 * timer overhead for small working sets (e.g., L1-resident arrays).
 */
double bench_sequential(const elem_t *arr, size_t n, size_t inner_iters) {
    double total = 0.0;
    for (size_t iter = 0; iter < inner_iters; iter++) {
        double s = 0.0;
        for (size_t i = 0; i < n; i++) {
            s += arr[i];
        }
        total += s;
    }
    return total;
}

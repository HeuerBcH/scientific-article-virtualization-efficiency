#include <stdio.h>
#include <time.h>

int main() {

    struct timespec res;

    clock_getres(CLOCK_MONOTONIC, &res);

    printf("Resolution: %ld ns\n", res.tv_nsec);

    return 0;
}

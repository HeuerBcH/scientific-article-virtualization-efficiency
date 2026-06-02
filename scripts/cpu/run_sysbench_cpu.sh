#!/bin/bash

OUTPUT=$1

echo "run,time_sec,events_per_sec" > $OUTPUT

for i in $(seq 1 30)
do

RESULT=$(sysbench cpu \
--cpu-max-prime=20000 \
run)

TIME=$(echo "$RESULT" | grep "total time:" | awk '{print $3}')

EVENTS=$(echo "$RESULT" | grep "events per second:" | awk '{print $4}')

echo "$i,$TIME,$EVENTS" >> $OUTPUT

done

# No Power Shell:
# rodar "wsl"
# rodar "chmod +x scripts/cpu/run_sysbench_cpu.sh"
# rodar "./scripts/cpu/run_sysbench_cpu.sh output.csv"
#!/bin/bash

OUTPUT=$1

echo "run,bogo_ops,bogo_ops_per_sec" > "$OUTPUT"

for i in $(seq 1 30)
do
    LINE=$(stress-ng --cpu 4 --timeout 10s --metrics-brief 2>&1 \
           | grep "metrc:" \
           | grep " cpu ")

    BOGO=$(echo "$LINE" | awk '{print $5}')
    BOGO_PER_SEC=$(echo "$LINE" | awk '{print $9}')

    echo "$i,$BOGO,$BOGO_PER_SEC" >> "$OUTPUT"

    echo "Run $i concluída"
done

# No Power Shell:
# rodar "wsl"
# rodar "chmod +x scripts/cpu/run_stressng_cpu.sh"
# rodar "./scripts/cpu/run_stressng_cpu.sh output.csv"
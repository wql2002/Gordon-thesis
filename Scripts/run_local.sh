#!/bin/bash

# TARGET_URL="10.10.0.10:8080"
TARGET_URL="172.31.20.50:8080"
TARGET_DN="local_reno"
TRIAL_S="1"
TRIAL_E="5"
DELAYS=("50" "70" "100")
# DELAYS=("50")

for delay in "${DELAYS[@]}"
do

    echo "[TEST] begin..."

    mm-delay ${delay} \
        /bin/bash \
        ./multi-launch.sh \
        ${TARGET_URL} \
        ${TRIAL_S} \
        ${TRIAL_E} \
        "${TARGET_DN}_${delay}"

    echo "[TEST] clean up..."
    ./clean.sh

done
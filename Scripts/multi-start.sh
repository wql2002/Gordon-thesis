#!/bin/bash

INPUT_FILE="../Alexa20k/cwnd_result.csv"

# check for file existence
if [ ! -f ${INPUT_FILE} ]; then
    echo "[ERROR] file not exists..."
    exit 1
fi

# read .csv file
line_num=0
while IFS=' ' read -r x y; do
    # check if the test done at this url
    if [ -z "$y" ]; then
        echo "[NOT DONE] ${x}"
        python3 start.py ${line_num}
    else
        echo "[DONE] ${x}, ${y}"
    fi
    ((line_num++))
done < ${INPUT_FILE}

echo "exp end..."
#!/usr/bin/env bash
DIR=./selenium
PYTHON_PATH=/Users/siarheis/venv/bin/python
#CHROME_PATH=$1
DT=$(date "+%Y%m%d-%H%M%S")
if [ -f $DIR/.running ]; then
    echo "Test is running"
    exit
fi
touch $DIR/.running
mkdir $DIR/.running.test
$PYTHON_PATH perf_test_selenium.py --out_dir=$DIR/.running.test --iterations=$1 &> $DIR/.running.test/output.log
#mv results.csv "results_$DT.csv"
#mv summary.csv "summary_$DT.csv"
mv $DIR/.running.test $DIR/$DT
rm $DIR/.running

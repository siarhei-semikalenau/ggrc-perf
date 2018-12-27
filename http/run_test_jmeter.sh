#!/usr/bin/env bash
DIR=./jmeter
PYTHON_PATH=/Users/siarheis/venv/bin/python
JMETER_PATH=/Users/siarheis/perf/apache-jmeter-5.0/bin/jmeter
#CHROME_PATH=$1
DT=$(date "+%Y%m%d-%H%M%S")
if [ -f $DIR/.running ]; then
    echo "Test is running"
    exit
fi
touch $DIR/.running
mkdir $DIR/.running.test
$JMETER_PATH -n -t perf_test_jmeter.jmx -Jout_dir=$DIR/.running.test -Jiter=$1 -j $DIR/.running.test/jmeter.log &> $DIR/.running.test/output.log
$PYTHON_PATH -c "import perf_utils; perf_utils.processResultsJmeter('$DIR/.running.test/results.csv', '$DIR/.running.test/summary.csv')"
mv $DIR/.running.test $DIR/$DT
rm $DIR/.running

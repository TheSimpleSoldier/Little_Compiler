#!/bin/bash

if [ "$1" = "-h" ]
then
    echo "Script to test output of compiler against proper output"
    echo "Usage: test.sh SCRIPTFILE BASEDIROFTESTS"
    exit 0
fi

script=$1
testdir=$2

if [ "$(echo -n $testdir | tail -c 1)" = "/" ]
then
    testdir=$(echo -n $testdir | rev | cut -c 2- | rev)
fi

basenames=($(ls "$testdir/inputs/"))

k=0
while [ $k -lt ${#basenames[@]} ]; do
    basename=$(echo ${basenames[$k]} | rev | cut -c 7- | rev)

    ./$script "$testdir/inputs/${basename}.micro" > "$testdir/outputs/${basename}.myout"

    echo
    echo $basename
    echo "=============================================================================="
    diff -b "$testdir/outputs/${basename}.out" "$testdir/outputs/${basename}.myout"

    let k=k+1;
done


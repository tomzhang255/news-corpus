#!/bin/bash

for j in `seq 43006325 43006327` ; do 
    scancel $j
    echo  $j
done

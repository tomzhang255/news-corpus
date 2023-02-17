#!/bin/bash

for j in `seq 41106726 41106774` ; do 
    scancel $j
    echo  $j
done

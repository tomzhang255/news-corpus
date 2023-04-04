#!/bin/bash

for j in `seq 43006325 43006334` ; do 
    scancel $j
    echo  $j
done

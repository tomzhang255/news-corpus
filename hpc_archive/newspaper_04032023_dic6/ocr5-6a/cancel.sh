#!/bin/bash

for j in `seq 44126589 44126935` ; do 
    scancel $j
    echo  $j
done

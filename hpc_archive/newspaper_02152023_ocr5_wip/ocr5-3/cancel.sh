#!/bin/bash

for j in `seq 41650432 41650452` ; do 
    scancel $j
    echo  $j
done

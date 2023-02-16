#!/bin/bash

for j in `seq 41181955 41181986` ; do 
    scancel $j
    echo  $j
done

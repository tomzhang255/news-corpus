#!/bin/bash

for j in `seq 41674598 41674636` ; do 
    scancel $j
    echo  $j
done

#!/bin/bash

for j in `seq 41674836 41674855` ; do 
    scancel $j
    echo  $j
done

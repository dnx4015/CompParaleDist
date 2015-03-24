#!/bin/sh
make -f Makefile $1 || exit
export OMP_NUM_THREADS=$2
./$1".out"



CC=g++
CFLAGS=-fopenmp
FILE?=mult

%:
	$(CC) $(CFLAGS) -o $* $*.cpp
	


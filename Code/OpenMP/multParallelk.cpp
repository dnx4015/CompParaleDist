/*
ID: diana.n1
PROG: MultParallelk
LANG: C++
*/

#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <assert.h>
#include <time.h>
#include "omp.h"

int main(int argc, char **argv) {
	double start, end; 
	start = omp_get_wtime();
    int nthreads, tid, chunk = 10;
	
	long **a, **b, **c;
    int N = 500;
	
    if (argc == 2) {
      N = atoi (argv[1]);
      assert (N > 0);
    }

    int i,j,k,mul=5;
    long col_sum = N * (N-1) / 2;
	long temp;
	
	a = (long **)malloc (N * sizeof(long *));
	b = (long **)malloc (N * sizeof(long *));
	c = (long **)malloc (N * sizeof(long *));
	
	for (i=0; i<N; i++) {
	  a[i] = (long *)malloc (N * sizeof(long));
	  b[i] = (long *)malloc (N * sizeof(long));
	  c[i] = (long *)malloc (N * sizeof(long));
	}

	#pragma omp parallel shared (a,b,c,nthreads, chunk, temp) private (i, j,k,tid)
	{
		tid = omp_get_thread_num();
		#pragma omp single
			printf("Number threads = %d\n", omp_get_num_threads());

		#pragma omp for schedule(static, chunk)
		for (i=0; i<N; i++){
			for (j=0; j<N; j++) {
				a[i][j] = i*mul;
				b[i][j] = i;
				c[i][j] = 0;
	  		}
		}
		#pragma omp single
			printf ("Matrix generation finished.\n");         
		
		for (i=0; i<N; i++){
			for (j=0; j<N; j++){
				#pragma omp single
					temp = 0;
				#pragma omp for schedule(static, chunk) reduction (+:temp) 
					for (k=0; k<N; k++){
						temp += a[i][k] * b[k][j];
					}
				#pragma omp single
					c[i][j] = temp;
		  	}
		}
		
		#pragma omp single
			printf ("Multiplication finished.\n");         
	
		#pragma omp for schedule(static, chunk)
			for (i=0; i<N; i++){
			  	for (j=0; j<N; j++){
					assert ( c[i][j] == i*mul * col_sum);  
				}
			}
		#pragma omp single
			printf ("Test finished.\n");         
	}

	end = omp_get_wtime();
	printf("Time: %lf.\n", end-start);
}


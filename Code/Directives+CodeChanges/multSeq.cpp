/*
ID: diana.n1
PROG: MultSeqCodeChange
LANG: C++
*/

#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <assert.h>
#include <time.h>
#include "omp.h"

void transpose(int n, long ** m){
	long tmp;
	for (int i = 0; i < n; i++){
		for (int j = i+1; j < n; j++){
			tmp = m[i][j];
			m[i][j] = m[j][i];
			m[j][i] = tmp;
		}
	}	
}

int main(int argc, char **argv) {
	double start, end; 
	start = omp_get_wtime();
	long **a, **b, **c;
    int N = 500;
	
    if (argc == 2) {
      N = atoi (argv[1]);
      assert (N > 0);
    }

    int i,j,k,mul=5;
    long col_sum = N * (N-1) / 2, tmp;
	
		
	a = (long **)malloc (N * sizeof(long *));
	b = (long **)malloc (N * sizeof(long *));
	c = (long **)malloc (N * sizeof(long *));
	for (i=0; i<N; i++) {
	  a[i] = (long *)malloc (N * sizeof(long));
	  b[i] = (long *)malloc (N * sizeof(long));
	  c[i] = (long *)malloc (N * sizeof(long));
	}


	for (i=0; i<N; i++){
	  for (j=0; j<N; j++) {
		a[i][j] = i*mul;
		b[i][j] = i;
		c[i][j] = 0;
	  }
	}

	printf ("Matrix generation finished.\n");         

	transpose(N, b);
	for (i=0; i<N; i++){
	  	for (j=0; j<N; j++){
			tmp = 0;
			for (k=0; k<N; k++){
				tmp += a[i][k] * b[j][k];
			}
			c[i][j] = tmp;
	  	}
	}

	printf ("Multiplication finished.\n");         
	
	for (i=0; i<N; i++)
	  for (j=0; j<N; j++)
		assert ( c[i][j] == i*mul * col_sum);  
    printf ("Test finished.\n");         

	end = omp_get_wtime();
	printf("Time: %lf.\n", end-start);
}


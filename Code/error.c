#include <stdio.h>
#include <omp.h>
//#define SIZE 46350
#define SIZE 16

int main(){

	int A[ SIZE ] , i ;
	#pragma omp parallel for schedule( static , 2 ) num_threads( 4 ) ordered
	for( i = 0 ; i < SIZE ; i++){
// Correccion, debe usarse tanto 'ordered clause' como 'ordered construct'
// Introducao ao OpenMP, pagina 50
		A[ i ] = i * i ;
		#pragma omp ordered
		{
			printf( "Th[ %d ]: %02d = %03d\n" , omp_get_thread_num() , i , A[ i ] ) ;
		}
	}
	return 0 ;
}

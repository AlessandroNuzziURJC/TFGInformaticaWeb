#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N 100000

int main() {
    int i;
    int sum = 0;
    int vector[N];
    srand(43);

    // Inicializar el vector con 100 números
    for (i = 1; i <= N; i++) {
        vector[i - 1] = rand()%100;
    }

    // Calcular la suma de los elementos del vector
    #pragma omp parallel for reduction(+:sum)
    for (i = 0; i < N; i++) {
        sum += vector[i];
    }

    printf("Suma total: %d\n", sum);

    return 0;
}
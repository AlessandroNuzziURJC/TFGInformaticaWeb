#include <stdio.h>
#include <stdlib.h>

#define N 100000

int main() {
    int i;
    int sum = 0;
    int vector[N];
    srand(43);

    // Inicializar el vector con los 100 primeros números
    for (i = 0; i < N; i++) {
        vector[i] = rand()%100;
    }

    // Calcular la suma de los elementos del vector
    for (i = 0; i < N; i++) {
        sum += vector[i];
    }

    printf("Suma total: %d\n", sum);

    return 0;
}
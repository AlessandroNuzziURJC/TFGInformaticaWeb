#include <stdio.h>
#include <mpi.h>
#include <stdlib.h>

#define N 100000

int main () {
    int rank, size;

    MPI_Status status;
    srand(43);

    MPI_Init(NULL, NULL);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    int arraySize[size];
    int * array;
    int sum = 0;
    int output = 0;
    int max = 0;

    //Calcular tamaño del array de cada hilo:
    if (rank == 0) {
        int val = N / size;
        for (int i = 0; i < size; i++) {
            arraySize[i] = val;
        }

        int mod = N % size;
        for (int i = 0; i < mod; i++) {
            arraySize[i]++;
        }

        max = arraySize[0];
        int* aux = (int*)malloc(max * sizeof(int));
        for (int j = 0; j < max; j++) {
            aux[j] = rand() % 100;
        }        
        array = aux;

        for (int i = 1; i < size; i++) {
            //MPI Send el tamaño del array
            MPI_Send(&arraySize[i], 1, MPI_INT, i, 0, MPI_COMM_WORLD);
            int aux[arraySize[i]];
            for (int j = 0; j < arraySize[i]; j++) {
                aux[j] = rand() % 100;
            }
            //MPI Send el array con los numeros
            MPI_Send(aux, arraySize[i], MPI_INT, i, 0, MPI_COMM_WORLD);
        }
    } else {
        //Recibo el tamaño del array
        MPI_Recv(&max, 1, MPI_INT, 0, 0,MPI_COMM_WORLD, &status);
        //Recibo el array
        int* aux = (int*)malloc(max * sizeof(int));
        MPI_Recv(aux, max, MPI_INT, 0, 0,MPI_COMM_WORLD, &status);
        array = aux;
    }

    // Inicializar el vector con 100 números
    for (int i = 0; i < max; i++) {
        sum += array[i];
    }
    if (rank != 0) {
        //Enviar resultado
        MPI_Send(&sum, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    } else {
        output = sum;
        for (int i = 1; i < size;i ++) {
            int value = 0;
            MPI_Recv(&value, 1, MPI_INT, i, 0,MPI_COMM_WORLD, &status);
            output += value;
        }

        printf("Suma total: %d\n", output);
    }

    free(array);

    MPI_Finalize();

}
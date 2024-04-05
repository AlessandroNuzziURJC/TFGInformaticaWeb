#include <stdio.h>
#include <mpi.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#define BOARD_SIZE 10000
#define ITERATION 10000

typedef struct{
    int rank;
    int size;
    int board_length;
} Process;

int ** initialize_board(int board_div) {
    
    int **board = (int **) malloc(sizeof(int*) * (board_div + 2));
    for (int i = 0; i < board_div + 2; i++) {
        board[i] = (int *)malloc(sizeof(int) * BOARD_SIZE);
    }

    for (int j = 0; j < BOARD_SIZE; j++) {
        board[0][j] = -1;
    }

    for (int j = 0; j < BOARD_SIZE; j++) {
        board[board_div + 1][j] = -1;
    }

    return board;
}

void generate_cells(int** board, Process *proc, int* divisions) {
    MPI_Status status;
    int partition = BOARD_SIZE/10;
    int* aux = (int*)malloc(sizeof(int) * partition); 
    if (proc->rank == 0) {
        for (int k = 0; k < proc->size; k++) {
            for (int i = 1; i < divisions[k] + 1; i++) {
                for (int l = 0; l < 10; l++) {
                    for (int j = 0 + l*partition; j < (l + 1)*partition; j++) {
                        if (k == 0) {
                            board[i][j] = rand()%2;
                        } else {
                            aux[j-l*partition] = rand()%2;
                        }
                    }
                    if (k != 0) {
                        MPI_Send(aux, partition, MPI_INT, k, 0, MPI_COMM_WORLD);
                    }
                }
            }
        }
    } else {
        for (int i = 1; i < proc->board_length + 1; i++) {
            for (int l = 0; l < 10; l++) {
                MPI_Recv(aux, partition, MPI_INT, 0, 0,MPI_COMM_WORLD, &status);
                for (int j = 0 + l*partition; j < (l + 1)*partition; j++) {
                    board[i][j] = aux[j-l*partition];
                }
            }
        }
    }
    free(aux);
}

int ** initialize_board_zero(int board_div) {
    int **board = (int **) malloc(sizeof(int*) * (board_div + 2));
    for (int i = 0; i < board_div + 2; i++) {
        board[i] = (int *)malloc(sizeof(int) * BOARD_SIZE);
    }

    for (int i = 1; i < board_div + 1; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j] = 0;
        }
    }

    for (int j = 0; j < BOARD_SIZE; j++) {
        board[0][j] = -1;
    }

    for (int j = 0; j < BOARD_SIZE; j++) {
        board[board_div + 1][j] = -1;
    }

    return board;
}

int* calculate_section(int size, int rank, int* rank_w) {
    MPI_Status status;
    if (rank == 0) {
        for (int i = 0; i < size; i++) {
            rank_w[i] = 0;
        }
        for (int i = 0; i < BOARD_SIZE; i++) {
            rank_w[i%size]++;
        }
        for (int i = 1; i < size; i++) {
            //MPI_Send(Valor de tablero)
            MPI_Send(rank_w, size, MPI_INT, i, 0, MPI_COMM_WORLD);
        }
        return rank_w;

    } else {
        MPI_Recv(rank_w, size, MPI_INT, 0, 0,MPI_COMM_WORLD, &status);
        return rank_w;
    }
}

void empty_board(int ** board, int length) {
    for (int i = 0; i < length + 2; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j] = 0;
        }
    }
        
    for (int j = 0; j < BOARD_SIZE; j++) {
        board[0][j] = -1;
    }

    for (int j = 0; j < BOARD_SIZE; j++) {
        board[length+ 1][j] = -1;
    }
}

int validate_position(int i, int j) {
    return i >= 0 && i < BOARD_SIZE && j >= 0 && j < BOARD_SIZE;
}

int check_life(int i, int j, int ** board) {
    int count = 0;

    for (int aux_i = -1; aux_i < 2; aux_i++) {
        for (int aux_j = -1; aux_j < 2; aux_j++) {
            if (aux_i != 0 || aux_j != 0) {
                if (validate_position(aux_i + i, aux_j + j) && board[aux_i + i][aux_j + j] == 1) {
                    count++;
                }
            }
        }
    }

    if (board[i][j] == 0 && count == 3)
        return 1;
    if (board[i][j] == 1 && (count == 3 || count == 2))
        return 1;
    else
        return 0;
}

void advance(int ** board, int **new_board, Process *proc) {
    MPI_Status status;
    int array_size = BOARD_SIZE / 10;
    if (proc->rank == 0) {
        for (int i = 0; i < 10; i++) {
            MPI_Send(board[proc->board_length] + i * array_size, array_size, MPI_INT, 1, 0,MPI_COMM_WORLD);
            MPI_Recv(board[proc->board_length + 1] + i * array_size, array_size, MPI_INT, 1, 0,MPI_COMM_WORLD, &status);
        }
    } else if (proc->rank == proc->size - 1) {
        for (int i = 0; i < 10; i++) {
            MPI_Send(board[1] + i * array_size, array_size, MPI_INT, proc->size - 2, 0,MPI_COMM_WORLD);
            MPI_Recv(board[0] + i * array_size, array_size, MPI_INT, proc->size - 2, 0,MPI_COMM_WORLD, &status);
        }
    } else {
        for (int i = 0; i < 10; i++) {
            MPI_Send(board[1] + i * array_size, array_size, MPI_INT, proc->rank - 1, 0,MPI_COMM_WORLD);
            MPI_Send(board[proc->board_length] + i * array_size, array_size, MPI_INT, proc->rank + 1, 0,MPI_COMM_WORLD);
            MPI_Recv(board[0] + i * array_size, array_size, MPI_INT, proc->rank - 1, 0,MPI_COMM_WORLD, &status);
            MPI_Recv(board[proc->board_length + 1] + i * array_size, array_size, MPI_INT, proc->rank + 1, 0,MPI_COMM_WORLD, &status);
        }
    }
    for (int i = 1; i < proc->board_length + 1; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            if (check_life(i, j, board)) {
                new_board[i][j] = 1;
            }
        }
    }
}


void free_memory(int ** matrix, Process *proc) {
    for (int i = 0; i < proc->board_length + 2; i++){
        free(matrix[i]);
    }

    free(matrix);
}

void print(int ** board, Process *proc) {
    MPI_Status status;
    FILE *outputFile;
    int check = 1;

    if (proc->rank == 0) {
        outputFile = fopen("output.txt", "w");
        for (int i = 1; i < proc->board_length + 1; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                fprintf(outputFile, "%d", board[i][j]);
            }
            fprintf(outputFile, "\n");
        }
        fclose(outputFile);
        MPI_Send(&check, 1, MPI_INT, 1, 0,MPI_COMM_WORLD);
    } else {
        MPI_Recv(board[proc->board_length + 1], BOARD_SIZE, MPI_INT, proc->rank - 1, 0,MPI_COMM_WORLD, &status);
        outputFile = fopen("output.txt", "a");
        for (int i = 1; i < proc->board_length + 1; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                fprintf(outputFile, "%d", board[i][j]);
            }
            fprintf(outputFile, "\n");
        }
        fclose(outputFile);
        if (proc->rank != proc->size - 1) {
            MPI_Send(&check, 1, MPI_INT, proc->rank + 1, 0,MPI_COMM_WORLD);
        }
    }
}

int main(int argc, char ** argv) {
    int rank, size;
    int board_div;
    int** board;
    int** new_board;
    int** aux;

    MPI_Init(NULL, NULL);
        
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    //Recibir el tamaño del tablero
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    srand(time(NULL) + rank);
    //srand(43);
    int rank_w[size];
    calculate_section(size, rank, rank_w);
    board_div = rank_w[rank];
    board = initialize_board(board_div);
    new_board = initialize_board_zero(board_div);

    Process process = {rank, size, board_div};
    generate_cells(board, &process, rank_w);

    for (int iteration = 0; iteration < ITERATION; iteration ++) {
        advance(board, new_board, &process);
        aux = board;
        board = new_board;
        new_board = aux;
        empty_board(new_board, board_div);
    }
    print(board, &process);
    MPI_Finalize();

    //Liberar memoria malloc
    free_memory(board, &process);
    free_memory(new_board, &process);

    return 0;
}
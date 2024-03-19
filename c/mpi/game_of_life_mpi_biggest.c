#include <stdio.h>
#include <mpi.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define BOARD_SIZE 1000
#define REPS 50000

typedef struct{
    int rank;
    int size;
    int board_length;
} Process;

int ** initialize_board(int board_div) {
    srand(43);
    int **board = (int **) malloc(sizeof(int*) * (board_div + 2));
    for (int i = 0; i < board_div + 2; i++) {
        board[i] = (int *)malloc(sizeof(int) * BOARD_SIZE);
    }

    for (int i = 1; i < board_div + 1; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j] = rand()%2;
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


int calculate_section(int size, int rank) {
    MPI_Status status;
    
    if (rank == 0) {
        int rank_w [size];
        for (int i = 0; i < size; i++) {
            rank_w[i] = 0;
        }
        for (int i = 0; i < BOARD_SIZE; i++) {
            rank_w[i%size]++;
        }
        for (int i = 1; i < size; i++) {
            //MPI_Send(Valor de tablero)
            MPI_Send(&rank_w[i], 1, MPI_INT, i, 0, MPI_COMM_WORLD);
        }
        return rank_w[0];

    } else {
        //Recibir bloqueante valor de tablero y devolverlo
        int val;

        MPI_Recv(&val, 1, MPI_INT, 0, 0,MPI_COMM_WORLD, &status);
        return val;
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

/*void print_board(int ** board, char* file_name, int length) {

    FILE* fichero;
    fichero = fopen(file_name, "a");
    for (int i = 0; i < length + 2; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            fprintf (fichero, "%d", board[i][j]);
        }
        fprintf(fichero, "%s", "\n");
    }
    fprintf(fichero, "%s", "\n");
    fclose(fichero);
}*/


void advance(int ** board, int **new_board, Process *proc) {
    MPI_Status status;
    if (proc->rank == 0) {
        MPI_Send(board[proc->board_length], BOARD_SIZE, MPI_INT, 1, 0,MPI_COMM_WORLD);
        MPI_Recv(board[proc->board_length + 1], BOARD_SIZE, MPI_INT, 1, 0,MPI_COMM_WORLD, &status);

        //Calcular avance
        for (int i = 1; i < proc->board_length + 1; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (check_life(i, j, board)) {
                    new_board[i][j] = 1;
                }
            }
        }
    } else if (proc->rank == proc->size - 1) {
        MPI_Send(board[1], BOARD_SIZE, MPI_INT, proc->size - 2, 0,MPI_COMM_WORLD);
        MPI_Recv(board[0], BOARD_SIZE, MPI_INT, proc->size - 2, 0,MPI_COMM_WORLD, &status);

        //Calcular avance
        for (int i = 1; i < proc->board_length + 1; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (check_life(i, j, board)) {
                    new_board[i][j] = 1;
                }
            }
        }
    } else {
        MPI_Send(board[1], BOARD_SIZE, MPI_INT, proc->rank - 1, 0,MPI_COMM_WORLD);
        MPI_Send(board[proc->board_length], BOARD_SIZE, MPI_INT, proc->rank + 1, 0,MPI_COMM_WORLD);
        MPI_Recv(board[0], BOARD_SIZE, MPI_INT, proc->rank - 1, 0,MPI_COMM_WORLD, &status);
        MPI_Recv(board[proc->board_length + 1], BOARD_SIZE, MPI_INT, proc->rank + 1, 0,MPI_COMM_WORLD, &status);
        
        //Calcular avance
        for (int i = 1; i < proc->board_length + 1; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (check_life(i, j, board)) {
                    new_board[i][j] = 1;
                }
            }
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
    board_div = calculate_section(size, rank);
    board = initialize_board(board_div);

    new_board = initialize_board_zero(board_div);

    Process process = {rank, size, board_div};

    for (int iteration = 0; iteration < REPS; iteration ++) {
        advance(board, new_board, &process);
        aux = board;
        board = new_board;
        new_board = aux;
        empty_board(new_board, board_div);
    }

    MPI_Finalize();

    return 0;
}
#include <stdio.h>
#include <mpi.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#define BOARD_SIZE 1000
#define ITERATION 1000

typedef struct{
    int rank;
    int size;
    int board_length;
} Process;

int ** initialize_board(int board_div, int rank) {
    srand(time(NULL) + rank);
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

int ** initialize_board_check(int board_div, int rank, int size) {
    MPI_Status status;
    int checked;
    if (rank == 0) {
        int** board = initialize_board(board_div, rank);
        checked = 1;
        MPI_Send(&checked, 1, MPI_INT, (rank+1)%size, 0, MPI_COMM_WORLD);
        return board;
    } else {
        MPI_Recv(&checked, 1, MPI_INT, rank-1, 0,MPI_COMM_WORLD, &status);
        int** board = initialize_board(board_div, rank);
        if ((rank+1)%size != 0) {
            checked = 1;
            MPI_Send(&checked, 1, MPI_INT, (rank+1)%size, 0, MPI_COMM_WORLD);
        }
        return board;
    }
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

/*void print(int ** board, Process *proc) {
    printf("Process %d\n", proc->rank);
    for (int i = 1; i < proc->board_length + 1; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            printf("%d", board[i][j]);
        }
        printf("\n");
    }
    printf("\n");
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
    board = initialize_board_check(board_div, rank, size);

    new_board = initialize_board_zero(board_div);

    Process process = {rank, size, board_div};

    for (int iteration = 0; iteration < ITERATION; iteration ++) {
        advance(board, new_board, &process);
        //print(board, &process);
        aux = board;
        board = new_board;
        new_board = aux;
        empty_board(new_board, board_div);
    }

    MPI_Finalize();

    return 0;
}
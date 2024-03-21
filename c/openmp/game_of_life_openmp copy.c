#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>
#define BOARD_SIZE 10

int ** initialize_board() {
    srand(1234);
    int **board = (int **) malloc(sizeof(int*) * BOARD_SIZE);
    for (int i = 0; i < BOARD_SIZE; i++) {
        board[i] = (int *)malloc(sizeof(int) * BOARD_SIZE);
    }

    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j] = rand()%2;
        }
    }

    return board;
}

int ** initialize_board_zero() {
    int **board = (int **) malloc(sizeof(int*) * BOARD_SIZE);
    for (int i = 0; i < BOARD_SIZE; i++) {
        board[i] = (int *)malloc(sizeof(int) * BOARD_SIZE);
    }

    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j] = 0;
        }
    }

    return board;
}

void empty_board(int ** board) {
    #pragma omp parallel
    {
        #pragma omp for
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                board[i][j] = 0;
            }
        }
    }
}

void print_board(int ** board, FILE * fichero) {
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            fprintf (fichero, "%d", board[i][j]);
        }
        fprintf(fichero, "%s", "\n");
    }
    fprintf(fichero, "%s", "\n");

}

int validate_position(int i, int j) {
    return i >= 0 && i < BOARD_SIZE && j >= 0 && j < BOARD_SIZE;
}

int check_life(int i, int j, int ** board) {
    int count = 0;

    for (int aux_i = -1; aux_i < 2; aux_i++) {
        for (int aux_j = -1; aux_j < 2; aux_j++) {
            if (aux_i != 0 || aux_j != 0) {
                if (validate_position(aux_i + i, aux_j + j) && board[aux_i + i][aux_j + j]) {
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

void advance(int ** board, int **new_board) {

    #pragma omp parallel
    {
        #pragma omp for
        for (int i = 0; i < BOARD_SIZE; i++) {
            for (int j = 0; j < BOARD_SIZE; j++) {
                if (check_life(i, j, board)) {
                    new_board[i][j] = 1;
                }
            }
        }
    }
}

void free_memory(int ** matrix) {
    for (int i = 0; i < BOARD_SIZE; i++){
        free(matrix[i]);
    }

    free(matrix);
}

int main(int argc, char *argv[]) {
    int threads = atoi(argv[1]);
    if (argc != 2 || threads == 0) {
        exit(1);
    }

    int** board;
    int** new_board;
    int** aux;

    omp_set_num_threads(threads);

    board = initialize_board_zero();
    board [0][1] = 1;
    board [1][2] = 1;
    board [2][0] = 1;
    board [2][1] = 1;
    board [2][2] = 1;
    new_board = initialize_board_zero();

    print_board(board, fichero);
    
    for (int iteration = 0; iteration < 1000; iteration ++) {
        advance(board, new_board);
        aux = board;
        board = new_board;
        new_board = aux;
        empty_board(new_board);
    }
    print_board(board, fichero);


    free_memory(board);
    free_memory(new_board);
    exit(0);
}
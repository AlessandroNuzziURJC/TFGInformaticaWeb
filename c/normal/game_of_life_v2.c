#include <stdio.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#define BOARD_SIZE 1000
#define ITERATION 1000

void initialize(int board[BOARD_SIZE][BOARD_SIZE]) {
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j] = rand()%2;
        }
    }
}

void initialize_zero(int board[BOARD_SIZE][BOARD_SIZE]) {
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            board[i][j] = 0;
        }
    }
}

void print(int board[BOARD_SIZE][BOARD_SIZE]) {
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            printf("%d", board[i][j]);
        }
        printf("\n");
    }
}

int validate_position(int i, int j) {
    return i >= 0 && i < BOARD_SIZE && j >= 0 && j < BOARD_SIZE;
}

int check_life(int i, int j, int board[BOARD_SIZE][BOARD_SIZE]) {
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

void advance(int board[BOARD_SIZE][BOARD_SIZE], int new_board[BOARD_SIZE][BOARD_SIZE]) {
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            if (check_life(i, j, board)) {
                new_board[i][j] = 1;
            }
        }
    }
}

void intercambiarMatrices(int (*matriz1)[BOARD_SIZE], int (*matriz2)[BOARD_SIZE]) {
    int (*aux)[BOARD_SIZE] = matriz1;
    memcpy(matriz1, matriz2, sizeof(int) * BOARD_SIZE * BOARD_SIZE);
    memcpy(matriz2, aux, sizeof(int) * BOARD_SIZE * BOARD_SIZE);
}

int main() {
    //Crear tablero actual
    int board1[BOARD_SIZE][BOARD_SIZE];
    //Crear tablero futuro
    int board2[BOARD_SIZE][BOARD_SIZE];
    //Inicializar con random
    srand(43);
    initialize(board1);
    initialize_zero(board2);

    //print(board1);

    for (int i = 0; i < ITERATION; i++) {
        //Calcular avance
        advance(board1, board2);
        //Cambiar tablero futuro por actual
        intercambiarMatrices(board1, board2);
        //Limpiar tablero antiguo conviertiendolo en tablero nuevo
        initialize_zero(board2);
    }

    //print(board1);
    //Guardar resultado en fichero de texto
}
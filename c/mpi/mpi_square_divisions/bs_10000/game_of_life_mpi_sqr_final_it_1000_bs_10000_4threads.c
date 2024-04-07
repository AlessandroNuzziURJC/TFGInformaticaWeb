#include <stdio.h>
#include <mpi.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#define BOARD_SIZE 10000
#define ITERATION 1000

typedef struct{
    int rank;
    int size;
    int board_length;
} Process;

int ** initialize_board(int board_div, int rank) {
    int **board = (int **) malloc(sizeof(int*) * (board_div + 2));
    for (int i = 0; i < board_div + 2; i++) {
        board[i] = (int *)malloc(sizeof(int) * (board_div + 2));
    }

    for (int i = 1; i < board_div + 1; i++) {
        board[i][0] = -1;
        board[i][board_div + 1] = -1;
    }

    for (int j = 0; j < board_div + 2; j++) {
        board[0][j] = -1;
    }

    for (int j = 0; j < board_div + 2; j++) {
        board[board_div + 1][j] = -1;
    }

    return board;
}

void generate_cells(int** board, Process *proc) {
    MPI_Status status;
    int aux[proc->board_length];
    int message_size = proc->board_length/5;
    if (proc->rank == 0) {
        for (int i = 1; i < proc->board_length + 1; i++) {
            for (int j = 1; j < proc->board_length + 1; j++) {
                board[i][j] = rand()%2;
            }
            for (int j = 0; j < proc->board_length; j++) {
                aux[j] = rand()%2;
            }
            for (int j = 0; j < 5; j++) {
                MPI_Send(aux + j*message_size, message_size, MPI_INT, 1, 0, MPI_COMM_WORLD);
            }
        }

        for (int i = 1; i < proc->board_length + 1; i++) {
            for (int j = 0; j < proc->board_length; j++) {
                aux[j] = rand()%2;
            }
            for (int j = 0; j < 5; j++) {
                MPI_Send(aux + j*message_size, message_size, MPI_INT, 2, 0, MPI_COMM_WORLD);
            }
            for (int j = 0; j < proc->board_length; j++) {
                aux[j] = rand()%2;
            }
            for (int j = 0; j < 5; j++) {
                MPI_Send(aux + j*message_size, message_size, MPI_INT, 3, 0, MPI_COMM_WORLD);
            }
        }
    } else {
        for (int i = 1; i < proc->board_length + 1; i++) {
            for (int j = 0; j < 5; j++) {
                MPI_Recv(aux + j*message_size, message_size, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);
            }
            for (int j = 1; j < proc->board_length + 1; j++) {
                board[i][j] = aux[j - 1];
            }
        }
    }
}

int ** initialize_board_zero(int board_div) {
    int **board = (int **) malloc(sizeof(int*) * (board_div + 2));
    for (int i = 0; i < board_div + 2; i++) {
        board[i] = (int *)malloc(sizeof(int) * board_div + 2);
    }

    for (int i = 1; i < board_div + 1; i++) {
        board[i][0] = -1;
        board[i][board_div + 1] = -1;
        for (int j = 1; j < board_div + 1; j++) {
            board[i][j] = 0;
        }
    }

    for (int j = 0; j < board_div + 2; j++) {
        board[0][j] = -1;
    }

    for (int j = 0; j < board_div + 2; j++) {
        board[board_div + 1][j] = -1;
    }

    return board;
}

int calculate_section(int size, int rank) {
    return BOARD_SIZE / 2;
}

void empty_board(int ** board, int length) {
    for (int i = 1; i < length + 1; i++) {
        board[i][0] = -1;
        board[i][length + 1] = -1;
        for (int j = 1; j < length + 1; j++) {
            board[i][j] = 0;
        }
    }
        
    for (int j = 0; j < length + 2; j++) {
        board[0][j] = -1;
    }

    for (int j = 0; j < length + 2; j++) {
        board[length+ 1][j] = -1;
    }
}

int validate_position(int i, int j) {
    return i >= 0 && i <= BOARD_SIZE/2 + 1 && j >= 0 && j <= BOARD_SIZE/2 + 1;
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
    int message_size = BOARD_SIZE / 10;
    int aux[proc->board_length + 2];
    if (proc->rank == 0) {
        for (int i = 0; i < 5; i++){
            MPI_Send(board[proc->board_length] + i * message_size, message_size, MPI_INT, 2, 0,MPI_COMM_WORLD);
            MPI_Recv(board[proc->board_length + 1] + i * message_size, message_size, MPI_INT, 2, 0,MPI_COMM_WORLD, &status);
        }
        MPI_Send(board[proc->board_length] + 5 * message_size, 2, MPI_INT, 2, 0,MPI_COMM_WORLD);
        MPI_Recv(board[proc->board_length + 1] + 5 * message_size, 2, MPI_INT, 2, 0,MPI_COMM_WORLD, &status);
        
        for (int i = 0; i < proc->board_length + 2; i++) {
            aux[i]=board[i][proc->board_length];
        }
        for (int i = 0; i < 5; i++){
            MPI_Send(aux + i * message_size, message_size, MPI_INT, 1, 0,MPI_COMM_WORLD);
            MPI_Recv(aux + i * message_size, message_size, MPI_INT, 1, 0,MPI_COMM_WORLD, &status);
        }
        
        MPI_Send(aux +  5 * message_size, 2, MPI_INT, 1, 0,MPI_COMM_WORLD);
        MPI_Recv(aux +  5 * message_size, 2, MPI_INT, 1, 0,MPI_COMM_WORLD, &status);
        for (int i = 0; i < proc->board_length + 2; i++) {
            board[i][proc->board_length + 1]=aux[i];
        }

    } else if (proc->rank == 1) {
        for (int i = 0; i < 5; i++){
            MPI_Send(board[proc->board_length]+ i * message_size, message_size, MPI_INT, 3, 0,MPI_COMM_WORLD);
            MPI_Recv(board[proc->board_length + 1]+ i * message_size, message_size, MPI_INT, 3, 0,MPI_COMM_WORLD, &status);
        }
        MPI_Send(board[proc->board_length] + 5 * message_size, 2, MPI_INT, 3, 0,MPI_COMM_WORLD);
        MPI_Recv(board[proc->board_length + 1] + 5 * message_size, 2, MPI_INT, 3, 0,MPI_COMM_WORLD, &status);
        
        for (int i = 0; i < proc->board_length + 2; i++) {
            aux[i]=board[i][1];
        }

        for (int i = 0; i < 5; i++){
            MPI_Send(aux + i * message_size, message_size, MPI_INT, 0, 0,MPI_COMM_WORLD);
            MPI_Recv(aux + i * message_size, message_size, MPI_INT, 0, 0,MPI_COMM_WORLD, &status);
        }
        MPI_Send(aux +  5 * message_size, 2, MPI_INT, 0, 0,MPI_COMM_WORLD);
        MPI_Recv(aux +  5 * message_size, 2, MPI_INT, 0, 0,MPI_COMM_WORLD, &status);

        for (int i = 0; i < proc->board_length + 2; i++) {
            board[i][0]=aux[i];
        }

    } else if (proc->rank == 2) {
        for (int i = 0; i < 5; i++){
            MPI_Send(board[1]+ i * message_size, message_size, MPI_INT, 0, 0,MPI_COMM_WORLD);
            MPI_Recv(board[0]+ i * message_size, message_size, MPI_INT, 0, 0,MPI_COMM_WORLD, &status);
        }
        MPI_Send(board[1]+ 5 * message_size, 2, MPI_INT, 0, 0,MPI_COMM_WORLD);
        MPI_Recv(board[0]+ 5 * message_size, 2, MPI_INT, 0, 0,MPI_COMM_WORLD, &status);
        
        for (int i = 0; i < proc->board_length + 2; i++) {
            aux[i]=board[i][proc->board_length];
        }
        for (int i = 0; i < 5; i++){
            MPI_Send(aux + i * message_size, message_size, MPI_INT, 3, 0,MPI_COMM_WORLD);
            MPI_Recv(aux + i * message_size, message_size, MPI_INT, 3, 0,MPI_COMM_WORLD, &status);
        }
        MPI_Send(aux + 5 * message_size, 2, MPI_INT, 3, 0,MPI_COMM_WORLD);
        MPI_Recv(aux + 5 * message_size, 2, MPI_INT, 3, 0,MPI_COMM_WORLD, &status);
        for (int i = 0; i < proc->board_length + 2; i++) {
            board[i][proc->board_length + 1]=aux[i];
        }

    } else if (proc->rank == 3) {
        for (int i = 0; i < 5; i++){
            MPI_Send(board[1] + i * message_size, message_size, MPI_INT, 1, 0,MPI_COMM_WORLD);
            MPI_Recv(board[0] + i * message_size, message_size, MPI_INT, 1, 0,MPI_COMM_WORLD, &status);
        }
        MPI_Send(board[1] + 5 * message_size, 2, MPI_INT, 1, 0,MPI_COMM_WORLD);
        MPI_Recv(board[0] + 5 * message_size, 2, MPI_INT, 1, 0,MPI_COMM_WORLD, &status);
        
        for (int i = 0; i < proc->board_length + 2; i++) {
            aux[i]=board[i][1];
        }

        for (int i = 0; i < 5; i++){
            MPI_Send(aux + i * message_size, message_size, MPI_INT, 2, 0,MPI_COMM_WORLD);
            MPI_Recv(aux + i * message_size, message_size, MPI_INT, 2, 0,MPI_COMM_WORLD, &status);
        }
        MPI_Send(aux + 5 * message_size, 2, MPI_INT, 2, 0,MPI_COMM_WORLD);
        MPI_Recv(aux + 5 * message_size, 2, MPI_INT, 2, 0,MPI_COMM_WORLD, &status);
        for (int i = 0; i < proc->board_length + 2; i++) {
            board[i][0]=aux[i];
        }
    }

    for (int i = 1; i < proc->board_length + 1; i++) {
        for (int j = 1; j < proc->board_length + 1; j++) {
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
        fclose(outputFile);
        for (int i = 1; i < proc->board_length + 1; i++) {
            outputFile = fopen("output.txt", "a");
            for (int j = 1; j < proc->board_length + 1; j++) {
                fprintf(outputFile, "%d", board[i][j]);
            }
            fclose(outputFile);
            MPI_Send(&check, 1, MPI_INT, 1, 0,MPI_COMM_WORLD);
            MPI_Recv(&check, 1, MPI_INT, 1, 0,MPI_COMM_WORLD, &status);
        }
        MPI_Send(&check, 1, MPI_INT, 2, 0,MPI_COMM_WORLD);
    } else if (proc->rank == 1) {
        for (int i = 1; i < proc->board_length + 1; i++) {
            MPI_Recv(&check, 1, MPI_INT, 0, 0,MPI_COMM_WORLD, &status);
            outputFile = fopen("output.txt", "a");
            for (int j = 1; j < proc->board_length + 1; j++) {
                fprintf(outputFile, "%d", board[i][j]);
            }
            fprintf(outputFile, "\n");
            fclose(outputFile);
            MPI_Send(&check, 1, MPI_INT, 0, 0,MPI_COMM_WORLD);
        }
    } else if (proc->rank == 2) {
        MPI_Recv(&check, 1, MPI_INT, 0, 0,MPI_COMM_WORLD, &status);
        for (int i = 1; i < proc->board_length + 1; i++) {
            outputFile = fopen("output.txt", "a");
            for (int j = 1; j < proc->board_length + 1; j++) {
                fprintf(outputFile, "%d", board[i][j]);
            }
            fclose(outputFile);
            MPI_Send(&check, 1, MPI_INT, 3, 0,MPI_COMM_WORLD);
            MPI_Recv(&check, 1, MPI_INT, 3, 0,MPI_COMM_WORLD, &status);
        }
    } else if (proc->rank == 3) {
        for (int i = 1; i < proc->board_length + 1; i++) {
            MPI_Recv(&check, 1, MPI_INT, 2, 0,MPI_COMM_WORLD, &status);
            outputFile = fopen("output.txt", "a");
            for (int j = 1; j < proc->board_length + 1; j++) {
                fprintf(outputFile, "%d", board[i][j]);
            }
            fprintf(outputFile, "\n");
            fclose(outputFile);
            MPI_Send(&check, 1, MPI_INT, 2, 0,MPI_COMM_WORLD);
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

    MPI_Comm_size(MPI_COMM_WORLD, &size);
    srand(time(NULL) + rank);
    //srand(43);

    board_div = calculate_section(size, rank);
    board = initialize_board(board_div, rank);
    new_board = initialize_board_zero(board_div);

    Process process = {rank, size, board_div};
    generate_cells(board, &process);

    for (int iteration = 0; iteration < ITERATION; iteration ++) {
        advance(board, new_board, &process);
        aux = board;
        board = new_board;
        new_board = aux;
        empty_board(new_board, board_div);
    }

    print(board, &process);
    free_memory(board, &process);
    free_memory(new_board, &process);
    MPI_Finalize();

    return 0;
}
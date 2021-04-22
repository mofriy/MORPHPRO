#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

#define VERT 1
#define HORIZ 2
#define DIAG 3

struct Alignment{
    int length;
    char *first;
    char *second;
};

struct Alignment needleman_wunsch(char *seq1, char *seq2, double gap_init_penalty, double gap_extend_penalty) {

    int n = strlen(seq1), m = strlen(seq2);

    // инициализируем scoring matrix
    double **score = (double **) malloc(sizeof(double *) * n);
    for(int i = 0; i < n; ++ i) {
        score[i] = (double *) malloc(sizeof(double) * m);
        for(int j = 0; j < m; ++ j) {
            score[i][j] = seq1[i] == seq2[j] ? 1.0 : 0.0;
        }
    }

    // инициализируем матрицы для динамики
    double ** mx_vert, **mx_horiz, **mx;
    mx_vert = (double **) malloc(sizeof(double*) * (n + 1));
    mx_horiz = (double **) malloc(sizeof(double*) * (n + 1));
    mx = (double **) malloc(sizeof(double*) * n);
    for(int i = 0; i <= n; ++ i) {
        mx_vert[i] = (double *)malloc(sizeof(double) * (m + 1));
        mx_horiz[i] = (double *)malloc(sizeof(double) * (m + 1));
        mx[i] = (double *)malloc(sizeof(double) * (m + 1));
    }

    // инициализируем backtrack
    int **backtrack = (int **) malloc(sizeof(int *) * (n + 1));
    for(int i = 0; i <= n; ++i) {
        backtrack[i] = (int *) malloc(sizeof(int) * (m + 1));
    }

    // запускаем динамику
    for(int i = 1; i <= n; ++ i) {
        for(int j = 1; j <= m; ++ j) {
            mx_vert[i][j] = fmax(mx_vert[i - 1][j] - gap_extend_penalty, 
                                 mx[i - 1][j] - (gap_init_penalty + gap_extend_penalty));
            mx_horiz[i][j] = fmax(mx_horiz[i][j - 1] - gap_extend_penalty, 
                                 mx[i][j - 1] - (gap_init_penalty + gap_extend_penalty));
            // проставляем возвраточку
            double v = mx_vert[i][j], h = mx_horiz[i][j], d = mx[i-1][j-1] + score[i-1][j-1];// минус единички на score, т.к. тут индексация относительно строк, т.е. начиная с нуля
            if (v >= h && v >= d) {
                mx[i][j] = v;
                backtrack[i][j] = VERT;
            } else if (h >= v && h >= d) {
                mx[i][j] = h;
                backtrack[i][j] = HORIZ;
            } else {
                mx[i][j] = d;
                backtrack[i][j] = DIAG;
            }
        }
    }

    
    // восстанавливаем ответ
    struct Alignment a;
    a.length = 0;
    a.first = (char *)malloc(sizeof(char) * (n + m + 1));
    a.second = (char *)malloc(sizeof(char) * (n + m + 1));
    int fp = 0, sp = 0;
    
    int pi = n, pj = m;
    while (pi > 0 && pj > 0) {
        int tmp = backtrack[pi][pj];
        switch (tmp) {
            case VERT:
                a.first[fp++] = seq1[pi - 1];
                a.second[sp++] = '-';
                --pi;
                break;
            case HORIZ:
                a.first[fp++] = '-';
                a.second[sp++] = seq2[pj - 1];
                --pj;
                break;
            case DIAG:
                a.first[fp++] = seq1[pi - 1];
                a.second[sp++] = seq2[pj - 1];
                --pi;--pj;
                break;
            default:
                exit(1);
                //todo
                break;
        }
    }

    for( ; pi > 0; -- pi) {
        a.first[fp++] = seq1[pi - 1];
        a.second[sp++] = '-';
    }

    for( ; pj > 0; --pj) {
        a.first[fp++] = '-';
        a.second[sp++] = seq2[pj - 1];
    }

    a.first = (char *)realloc(a.first, sizeof(char) * (fp + 1));
    a.second = (char *)realloc(a.second, sizeof(char) * (sp + 1));
    a.length = fp;
    #ifdef DEBUG
    printf("DEBUG %d\n%s\n%s\n", a.length, a.first, a.second);
    #endif
    return a;
}

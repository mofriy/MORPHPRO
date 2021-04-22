/*
    INPUT:
    на первой строчке - два числа, длины первой и второй строки в символах соответственно
    на второй строчке - первая выравниваемая строка
    на третьей строчке - вторая выравниваемая строка

    OUTPUT:
    На первой строчке - количество match'ей после выравнивания двух строк
    на второй строчки - индексы элементов из первой входной строки, которые поматчились
    на третьей строчке - индексы элементов из второй входной строки, которые поматчились

    SAMPLE:
    IN:
3 3
aba
bab
    OUT:
2
0 1
1 2
*/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "needleman.h"

//Alignment needleman_wunsch(char *seq1, char *seq2, double gap_init_penalty, double gap_extend_penalty);

int main(int argc, char *argv[]) {
	int n, m;
	
	if (argc == 1){
		scanf("%d %d\n", &n, &m);
	} else {
		n = strlen(argv[1]);
		m = strlen(argv[2]);
	}
	char seq1[n+1], seq2[m + 1];
	if (argc == 1)
		scanf("%s%s", seq1, seq2);
	else {
		strcpy(seq1, argv[1]);
		strcpy(seq2, argv[2]);
	}
    // выравнили цепочки
    struct Alignment ans = needleman_wunsch(seq1, seq2, 1.0, 0.1);
    
    int len = ans.length;
    // посчитали количество matches
    int nn = 0;
    for(int i = 0; i < len; i ++) {
        if (ans.first[i] == ans.second[i]) ++nn;
    }

    // индексные массивы
    int indexes_first[nn], indexes_second[nn];

    // поправки на gap'ы
    int shift_first = 0, shift_second = 0;
    nn = 0;
    // заполняем индексные массивы
    for(int i = 0; i < len; i ++) {
        if (ans.first[i] == '-') ++shift_first; else
        if (ans.second[i] == '-') ++shift_second; else
        if (ans.first[i] == ans.second[i]) {
            indexes_first[nn] = i - shift_first;
            indexes_second[nn] = i - shift_second;
            ++nn;
        }
    }

    //printf("%s\n%s\n", ans.first, ans.second);
    
    printf("%d\n", nn);
    for(int i = 0; i < nn; i ++) {
        printf("%d ", indexes_first[i]);
    }
    printf("\n");
    for(int i = 0; i < nn; i ++) {
        printf("%d ", indexes_second[i]);
    }
    printf("\n");
    return 0;
}


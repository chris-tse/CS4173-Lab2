#include <stdio.h>
#include <stdlib.h>
#include <openssl/aes.h>
#define KEYSIZE 16

void main()
{
    int i;
    char key[KEYSIZE];
    FILE* file;
    file = fopen("keys.txt", "w");

    if (file == NULL) {
        fprintf(stderr, "Could not open file keys.txt");
        exit(1);
    }
    int startingTime = 1524017329;
    for (int i = startingTime; i <= startingTime + 7200; i++) {
        srand(i);
        for (int i = 0; i < KEYSIZE; i++) {
            key[i] = rand() % 256;
            fprintf(file, "%.2x", (unsigned char)key[i]);
        }
        fprintf(file, "\n");
    }

    fclose(file);
}
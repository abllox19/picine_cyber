#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void ok(void) {
    puts("Good job.");
}

void no(void) {
    puts("Nope.");
    exit(1);
}

int main(void) {
    char input[24] = {0};
    char decoded_str[9] = {0};
    
    printf("Please enter key: ");
    if (scanf("%23s", input) != 1) {
        no();
    }
    
    // La clé doit obligatoirement commencer par "00"
    if (input[0] != '0' || input[1] != '0') {
        no();
    }
    
    // Construction de la chaîne à comparer
    decoded_str[0] = 'd';
    int in_idx = 2;
    int out_idx = 1;
    
    // Boucle qui lit les caractères restants par paquets de 3
    while (out_idx < 8 && in_idx < strlen(input)) {
        char chunk[4] = {0}; // Buffer temporaire pour stocker 3 chiffres
        
        chunk[0] = input[in_idx];
        chunk[1] = input[in_idx + 1];
        chunk[2] = input[in_idx + 2];
        
        // Convertit les 3 chiffres en entier, puis en caractère ASCII
        decoded_str[out_idx] = (char)atoi(chunk);
        
        in_idx += 3;
        out_idx++;
    }
    
    decoded_str[out_idx] = '\0';
    
    // Vérification finale
    if (strcmp(decoded_str, "delabere") == 0) {
        ok();
    } else {
        no();
    }
    
    return 0;
}

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
    char input[31] = {0};
    char decoded_str[9] = {0};
    
    printf("Please enter key: ");
    if (scanf("%30s", input) != 1) {
        no();
    }
    
    // La clé doit obligatoirement commencer par "42"
    if (input[0] != '4' || input[1] != '2') {
        no();
    }
    
    // Initialisation du premier caractère avec '*'
    decoded_str[0] = '*';
    int in_idx = 2;
    int out_idx = 1;
    
    // Décodage par paquets de 3 chiffres
    while (out_idx < 8 && in_idx < strlen(input)) {
        char chunk[4] = {0}; 
        
        chunk[0] = input[in_idx];
        chunk[1] = input[in_idx + 1];
        chunk[2] = input[in_idx + 2];
        
        decoded_str[out_idx] = (char)atoi(chunk);
        
        in_idx += 3;
        out_idx++;
    }
    
    decoded_str[out_idx] = '\0';
    
    // Vérification finale
    if (strcmp(decoded_str, "********") == 0) {
        ok();
    } else {
        no();
    }
    
    return 0;
}

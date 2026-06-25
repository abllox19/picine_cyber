import argparse
import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from PIL import Image
from PIL.ExifTags import TAGS 

def Extraction_img(img_path):
    try:
        image = Image.open(img_path)
        
        print(f"--- Analyse de : {img_path} ---")
        print(f"Format : {image.format}")
        print(f"Taille : {image.size} (Largeur, Hauteur)")
        print(f"Mode de couleur : {image.mode}")

        info_exif = image.getexif()
        
        if not info_exif:
            print("Aucune donnée EXIF trouvée.")
        else:
            print("\nDonnées EXIF :")
            for tag_id, value in info_exif.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if isinstance(value, bytes) and len(value) > 50:
                    value = f"<{len(value)} bytes>"
                print(f"  {tag_name}: {value}")

        image.show()

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{img_path}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur lors du traitement de l'image : {e}")

def main():
    if len(sys.argv) == 1:
        print("Usage: python scorpion.py image1.jpg image2.png ...")
        sys.exit(1)

    tableau_arguments = sys.argv[1:]

    for i, img in enumerate(tableau_arguments):
        Extraction_img(img)
        print("\n" + "_"*40 + "\n")

if __name__ == "__main__":
    main()
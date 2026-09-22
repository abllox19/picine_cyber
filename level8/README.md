# Vaccine

`Vaccine` est un outil d'audit en ligne de commande développé en Python permettant de détecter la présence de vulnérabilités d'injection SQL (SQLi) et d'identifier le système de gestion de base de données (SGBD) sous-jacent.

Ce projet a été réalisé dans le cadre de la Cybersecurity Piscine (42).

---

## Fonctionnalités

- **Méthodes HTTP** : Prise en charge des requêtes `GET` et `POST` via l'option `-X`.
- **Gestion des sessions** : Injection de cookies HTTP d'authentification via l'option `-c`.
- **Rapport d'audit** : Sauvegarde automatique des résultats dans un fichier d'archive via l'option `-o` (par défaut `vaccine_report.txt`).
- **Méthodes d'injection détectées** :
  - *Error-based SQLi* (détection via rupture syntaxique et regex de signatures d'erreurs).
  - *Boolean-based SQLi* (analyse différentielle entre requêtes logiques vraies et fausses).
- **SGBD identifiés** :
  - MySQL / MariaDB
  - SQLite

---

## Architecture du projet

Le projet est conçu de manière monolithique dans un script unique `vaccine` pour simplifier l'exécution et l'évaluation :

- `NetworkClient` : Encapsule les sessions HTTP `requests`, gère les en-têtes, les cookies de session et l'envoi transparent en `GET` ou `POST`.
- `ResponseAnalyzer` : Stocke la réponse saine de référence (*baseline*) et applique les expressions régulières pour identifier les moteurs de bases de données.
- `scan_target` : Parcourt les paramètres d'URL, injecte les sondes de test et analyse les réponses HTTP obtenues.
- `save_report` : Écrit et archive les résultats au format texte structuré et horodaté.

---

## Prérequis & Installation

- Python 3.9 ou supérieur
- Bibliothèque standard et module `requests` :

```bash
pip install requests

chmod +x vaccine

# Démarrer le conteneur DVWA
make up

# Stopper le conteneur
make down

# Nettoyer les volumes et conteneurs
make clean

usage: ./vaccine [-o OUTPUT] [-X METHOD] [-c COOKIE] URL

# Exemple:

./vaccine "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit"

./vaccine -c "PHPSESSID=abcdef123456; security=low" "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit"

./vaccine -c "PHPSESSID=abcdef123456; security=low" -o audit_dvwa.txt -X POST "http://localhost:8080/vulnerabilities/sqli/?id=1&Submit=Submit"
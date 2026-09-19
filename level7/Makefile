COMPOSE = docker compose

.PHONY: all up down build clean re sh-inquisitor sh-client sh-server test-ftp tables

all: up

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

clean:
	$(COMPOSE) down -v --remove-orphans

re: clean up

# Accès shell direct aux machines
sh-inquisitor:
	$(COMPOSE) exec inquisitor bash

sh-client:
	$(COMPOSE) exec client sh

sh-server:
	$(COMPOSE) exec server sh

# Affiche les tables ARP des deux cibles
tables:
	@echo "=== Table ARP du Client ==="
	@$(COMPOSE) exec client ip neigh
	@echo "\n=== Table ARP du Serveur ==="
	@$(COMPOSE) exec server ip neigh

# Simule une connexion FTP légitime depuis le client
test-ftp:
	@$(COMPOSE) exec client which lftp > /dev/null 2>&1 || $(COMPOSE) exec client apk add --no-cache lftp
	$(COMPOSE) exec client lftp -u victim,PiscineCyber42 172.20.0.10 -e "ls; bye"

# Simule le dépôt et le téléchargement d'un fichier pour valider la détection des noms
test-transfer:
	@$(COMPOSE) exec client which lftp > /dev/null 2>&1 || $(COMPOSE) exec client apk add --no-cache lftp
	@echo "--- Création d'un fichier de test sur le client ---"
	@$(COMPOSE) exec client sh -c "echo 'TopSecretData42' > /tmp/flag.txt"
	@echo "--- Envoi du fichier (STOR) ---"
	@$(COMPOSE) exec client lftp -u victim,PiscineCyber42 172.20.0.10 -e "put /tmp/flag.txt; bye"
	@echo "--- Récupération du fichier (RETR) ---"
	@$(COMPOSE) exec client lftp -u victim,PiscineCyber42 172.20.0.10 -e "get flag.txt -o /tmp/downloaded_flag.txt; bye"
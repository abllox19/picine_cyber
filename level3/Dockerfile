FROM alpine:latest

# Installation des paquets nécessaires
RUN apk update && apk add tor nginx openssh

# Configuration de base SSH (Génération des clés hôtes et création d'un mot de passe root)
RUN ssh-keygen -A
RUN echo 'root:root' | chpasswd

# Création des dossiers nécessaires
RUN mkdir -p /var/www/html /run/nginx /var/lib/tor/hidden_service/

# Copie des fichiers de configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY sshd_config /etc/ssh/sshd_config
COPY torrc /etc/tor/torrc
COPY index.html /var/www/html/index.html

# Droits stricts pour Tor (Requis par le daemon Tor)
RUN chown -R tor:tor /var/lib/tor/
RUN chmod 700 /var/lib/tor/hidden_service/

# Copie du script de démarrage
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# REMARQUE : Aucun port n'est exposé (Pas de commande EXPOSE)
CMD ["/entrypoint.sh"]
#!/bin/sh

# Démarrage de SSHD en arrière-plan
/usr/sbin/sshd

# Démarrage de Nginx en arrière-plan
nginx

# Démarrage de Tor au premier plan (garde le conteneur en vie)
exec tor -f /etc/tor/torrc
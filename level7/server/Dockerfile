FROM alpine:3.19

RUN apk update && apk add --no-cache vsftpd linux-pam iproute2

# Création du dossier secure_chroot_dir et de l'utilisateur avec shell valide
RUN mkdir -p /var/run/vsftpd/empty /home/victim && \
    adduser -s /bin/sh -D -h /home/victim victim && \
    echo "victim:PiscineCyber42" | chpasswd && \
    chown -R victim:victim /home/victim

# Configuration PAM standard pour vsftpd (authentification locale via /etc/shadow)
RUN echo -e "auth required pam_unix.so\naccount required pam_unix.so" > /etc/pam.d/vsftpd

COPY vsftpd.conf /etc/vsftpd/vsftpd.conf

EXPOSE 21 21100-21110

CMD ["vsftpd", "/etc/vsftpd/vsftpd.conf"]
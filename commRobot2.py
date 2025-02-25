# -*- coding: utf-8 -*-
import socket

# Configurations IP des robots
MY_IP = "192.168.0.115"  # À remplacer par l'IP du robot exécutant le script
TARGET_IP = "192.168.0.110"  # À remplacer par l'IP du robot destinataire
PORT = 5005  # Port UDP (doit être identique sur les 2 robots)

def udp_communication():
    # Création du socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((MY_IP, PORT))  # Liaison à l'adresse locale

    # Réception de la réponse
    print("En attente d'un message...")
    data, addr = sock.recvfrom(1024)  # Réception d'un paquet (1024 octets max)
    print("Message reçu de {} : {}".format(addr[0], data))

    # Envoi de la réponse
    response = "Salut!"
    print("Réponse envoyée : {}".format(response))
    sock.sendto(response, addr)

    # Fermeture du socket
    sock.close()

if __name__ == "__main__":
    udp_communication()

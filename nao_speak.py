# -*- coding: utf-8 -*-

from naoqi import ALProxy

# Adresse IP du robot NAO
if __name__ == "__main__":
    NAO_IP = "192.168.143.30"  # Remplace par l'IP du NAO
    NAO_PORT = 9559

# Connexion au module de synthèse vocale
tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
tts.setLanguage("French")
# Faire parler le robot
tts.say("Bonjour, je suis NAO !")

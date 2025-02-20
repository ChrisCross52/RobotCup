# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time

# Connexion au robot
robot_ip = "192.168.0.110"
port = 9559

# Initialisation des proxys
vision = ALProxy("ALVisionRecognition", robot_ip, port)
memory = ALProxy("ALMemory", robot_ip, port)  # ALMemory permet de lire les résultats
tts = ALProxy("ALTextToSpeech", robot_ip, port)
motion = ALProxy("ALMotion", robot_ip, port)

# Réveiller NAO
motion.wakeUp()

# Activer la reconnaissance d'images
vision.subscribe("VisionRecognitionTest")
print("Recherche d'images en cours...")

while True:
    # Lire les résultats de la reconnaissance dans la mémoire de NAO
    data = memory.getData("PictureDetected")

    if data and isinstance(data, list) and len(data) > 0:
        detected_labels = [item[0] for item in data[1]]  # Récupérer les noms des images reconnues
        
        if detected_labels:
            print("Image(s) reconnue(s)")
            tts.say("J'ai reconnu")

    time.sleep(1)  # Pause pour éviter de surcharger NAO

# Désactiver la reconnaissance après utilisation
vision.unsubscribe("VisionRecognitionTest")

# Mettre NAO en repos
motion.rest()

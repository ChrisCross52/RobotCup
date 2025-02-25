# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time
import re  # Pour extraire la valeur de distance depuis le nom de l'image
import math  # Pour convertir les degrés en radians

# Connexion au robot
robot_ip = "192.168.0.110"
port = 9559

# Initialisation des proxys
vision = ALProxy("ALVisionRecognition", robot_ip, port)
memory = ALProxy("ALMemory", robot_ip, port)
tts = ALProxy("ALTextToSpeech", robot_ip, port)
motion = ALProxy("ALMotion", robot_ip, port)

# Réveiller NAO
motion.wakeUp()

# Activer la reconnaissance d'images
vision.subscribe("VisionRecognitionTest")
print("Recherche d'images en cours...")

# Initialisation
qr_detected = False
distance = 0  # Distance à parcourir après reconnaissance
image_name = ""
rotation_angle = 45  # Degré par étape
rotation_radian = math.radians(rotation_angle)  # Conversion en radians

while not qr_detected:
    # Tourne de 45° vers la gauche
    motion.moveTo(0, 0, rotation_radian)
    
    # Attendre 2 secondes pour l'analyse
    time.sleep(2)

    # Vérifier s'il y a une image reconnue
    data = memory.getData("PictureDetected")

    if data and isinstance(data, list) and len(data) > 1:
        detected_labels = [item[0] for item in data[1]]  # Récupérer les noms des images reconnues
        
        if detected_labels:
            image_name = detected_labels[0]  # On prend le premier élément reconnu
            print("Image reconnue : {}".format(image_name))
            tts.say("J'ai reconnu une image")

            # Sauvegarder le nom du fichier dans un fichier texte
            with open("/home/nao/recognized_image.txt", "w") as file:
                file.write(image_name)

            # Extraire la distance depuis le nom du fichier (ex: "20.png" -> 20)
            match = re.search(r"(\d+)", image_name)  # Recherche d'un nombre dans le nom
            if match:
                distance = int(match.group(1)) / 100.0  # Convertir en mètres
                qr_detected = True
                break  # Sortir de la boucle une fois la correspondance trouvée

# Arrêter NAO de tourner
motion.stopMove()

# Faire avancer NAO vers l'objet reconnu
if distance > 0:
    print("Avancement de {} mètres".format(distance))
    tts.say("J'avance de {} mètres".format(distance))
    motion.moveTo(distance, 0, 0)  # Avancer selon la distance extraite

# Désactiver la reconnaissance après utilisation
vision.unsubscribe("VisionRecognitionTest")

# Mettre NAO en repos
motion.rest()
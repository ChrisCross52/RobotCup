# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time
import re  # Pour extraire la valeur de distance depuis le nom de l'image

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

# Faire tourner NAO jusqu'à reconnaissance
# motion.setAngles("HeadYaw", 0.0, 0.1)  # Centre la tête
# motion.move(0, 0, 0.5)  # NAO tourne sur lui-même à vitesse angulaire de 0.5 rad/s

qr_detected = False
distance = 0  # Distance à parcourir après reconnaissance
image_name = ""

while not qr_detected:
    data = memory.getData("PictureDetected")

    if data and isinstance(data, list) and len(data) > 1:
        detected_labels = [item[0] for item in data[1]]  # Récupérer les noms des images reconnues
        
        if detected_labels:
            image_name = detected_labels[0]  # On prend le premier élément reconnu
            print("Image reconnue : {}".format(image_name))
            
            # Sauvegarder le nom du fichier dans un fichier texte
            with open("/home/nao/recognized_image.txt", "w") as file:
                file.write(image_name)

            # Extraire la distance depuis le nom du fichier (ex: "20.png" -> 20)
            match = re.search(r"(\d+)", image_name)  # Recherche d'un nombre dans le nom
            if match:
                distance = int(match.group(1)) / 100.0  # Convertir en mètres
                qr_detected = True
                # motion.stopMove()  # Arrêter la rotation

    time.sleep(0.5)  # Vérification toutes les 500ms

# Faire avancer NAO vers l'objet reconnu
if distance > 0:
    print("Avancement de {} mètres".format(distance))
    motion.moveTo(distance, 0, 0)  # Avancer selon la distance extraite

# Désactiver la reconnaissance après utilisation
vision.unsubscribe("VisionRecognitionTest")

# Mettre NAO en repos
motion.rest()
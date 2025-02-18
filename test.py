# -*- coding: utf-8 -*-

from naoqi import ALProxy  # Importation de la bibliothèque permettant de contrôler NAO
import time  # Importation du module time pour ajouter des pauses entre les actions


def nao_wake_up(nao_ip, nao_port):
    """Réveille NAO et initialise sa posture"""
    motion = ALProxy("ALMotion", nao_ip, nao_port)  # Création d'un proxy pour contrôler le mouvement de NAO
    posture = ALProxy("ALRobotPosture", nao_ip, nao_port)  # Création d'un proxy pour gérer la posture de NAO
    motion.wakeUp()  # Réveille NAO
    posture.goToPosture("StandInit", 1.0)  # Met NAO en posture initiale
    print("NAO est réveillé et en position initiale.")


def nao_walk(nao_ip, nao_port):
    """Fait marcher NAO de 0.5 mètre en avant"""
    motion = ALProxy("ALMotion", nao_ip, nao_port)  # Création d'un proxy pour le mouvement
    motion.moveTo(0.5, 0, 0)  # Fait avancer NAO de 0.5 mètre en ligne droite
    print("NAO a marché de 0.5 mètre en avant.")


def nao_raise_right_arm(nao_ip, nao_port):
    """Lève le bras droit de NAO"""
    motion = ALProxy("ALMotion", nao_ip, nao_port)  # Création d'un proxy pour le mouvement
    names = ["RShoulderPitch", "RShoulderRoll"]  # Liste des articulations du bras droit à manipuler
    angles = [-0.5, -0.2]  # Angles définis pour lever le bras droit
    motion.setAngles(names, angles, 0.2)  # Applique les angles avec une vitesse d'exécution
    print("NAO a levé son bras droit.")


def nao_raise_left_arm(nao_ip, nao_port):
    """Lève le bras gauche de NAO"""
    motion = ALProxy("ALMotion", nao_ip, nao_port)  # Création d'un proxy pour le mouvement
    names = ["LShoulderPitch", "LShoulderRoll"]  # Liste des articulations du bras gauche à manipuler
    angles = [-0.5, 0.2]  # Angles définis pour lever le bras gauche
    motion.setAngles(names, angles, 0.2)  # Applique les angles avec une vitesse d'exécution
    print("NAO a levé son bras gauche.")


def nao_speak(nao_ip, nao_port, text="Bonjour, je suis NAO!"):
    """Fait parler NAO"""
    tts = ALProxy("ALTextToSpeech", nao_ip, nao_port)  # Création d'un proxy pour la synthèse vocale
    tts.say(text)  # NAO prononce le texte donné
    print("NAO a dit:", text)


def nao_sit_down(nao_ip, nao_port):
    """Fait s'asseoir NAO"""
    posture = ALProxy("ALRobotPosture", nao_ip, nao_port)  # Création d'un proxy pour gérer la posture
    posture.goToPosture("Sit", 1.0)  # Met NAO en position assise
    motion = ALProxy("ALMotion", nao_ip, nao_port)  # Création d'un proxy pour le mouvement
    motion.rest()  # Désactive les moteurs pour économiser l'énergie
    print("NAO est assis et au repos.")


if __name__ == "__main__":
    NAO_IP = "192.168.143.30"  # Remplacez par l'adresse IP de votre NAO
    NAO_PORT = 9559

    nao_wake_up(NAO_IP, NAO_PORT)  # Réveille NAO
    time.sleep(2)  # Pause de 2 secondes
    nao_walk(NAO_IP, NAO_PORT)  # Fait marcher NAO
    time.sleep(2)  # Pause de 2 secondes
    nao_raise_right_arm(NAO_IP, NAO_PORT)  # Lève le bras droit
    time.sleep(2)  # Pause de 2 secondes
    nao_raise_left_arm(NAO_IP, NAO_PORT)  # Lève le bras gauche
    time.sleep(2)  # Pause de 2 secondes
    nao_speak(NAO_IP, NAO_PORT, "Je peux faire plusieurs mouvements!")  # NAO parle
    time.sleep(2)  # Pause de 2 secondes
    nao_sit_down(NAO_IP, NAO_PORT)  # Fait s'asseoir NAO

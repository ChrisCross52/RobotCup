# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time
import math

robot_ip = "192.168.0.110"
port = 9559

# Initialisation des proxys
motion_proxy = ALProxy("ALMotion", robot_ip, port)
posture_proxy = ALProxy("ALRobotPosture", robot_ip, port)
memory_proxy = ALProxy("ALMemory", robot_ip, port)  # Accès aux capteurs de pression
imu_proxy = ALProxy("ALMotion", robot_ip, port)  # Accéléromètre/Gyroscope

motion_proxy.wakeUp()
posture_proxy.goToPosture("StandInit", 0.5)

def calculate_zmp():
    """ Calcule le Zero-Moment Point (ZMP) basé sur les capteurs de pression. """
    left_sensors = [
        "Device/SubDeviceList/LFoot/FSR/FrontLeft/Sensor/Value",
        "Device/SubDeviceList/LFoot/FSR/FrontRight/Sensor/Value",
        "Device/SubDeviceList/LFoot/FSR/RearLeft/Sensor/Value",
        "Device/SubDeviceList/LFoot/FSR/RearRight/Sensor/Value"
    ]
    right_sensors = [
        "Device/SubDeviceList/RFoot/FSR/FrontLeft/Sensor/Value",
        "Device/SubDeviceList/RFoot/FSR/FrontRight/Sensor/Value",
        "Device/SubDeviceList/RFoot/FSR/RearLeft/Sensor/Value",
        "Device/SubDeviceList/RFoot/FSR/RearRight/Sensor/Value"
    ]
    
    left_foot = sum([memory_proxy.getData(sensor) for sensor in left_sensors])
    right_foot = sum([memory_proxy.getData(sensor) for sensor in right_sensors])
    total_force = left_foot + right_foot
    
    if total_force == 0:
        return None  # NAO est en l'air ou chute
    
    zmp_x = (left_foot * -0.02 + right_foot * 0.02) / total_force  # Approximation
    zmp_y = 0  # Supposition que le ZMP est aligné sur l'axe central
    
    return zmp_x, zmp_y

def balance_and_kick(duration=3):
    """ Maintient NAO en équilibre sur une jambe et effectue un tir avec l'autre jambe. """
    # Étape 1 : Déplacement du poids vers la jambe gauche
    names = ["LHipRoll", "RHipRoll", "LAnkleRoll", "RAnkleRoll"]
    angles = [math.radians(10), math.radians(-20), math.radians(5), math.radians(-5)]
    motion_proxy.setAngles(names, angles, 0.2)
    time.sleep(1)  # Pause pour stabiliser

    # Étape 2 : Lever la jambe droite
    names = ["RHipPitch", "RKneePitch", "RAnklePitch"]
    angles = [math.radians(-10), math.radians(30), math.radians(-10)]
    motion_proxy.setAngles(names, angles, 0.2)
    
    start_time = time.time()
    while time.time() - start_time < duration:
        imu_data = imu_proxy.getAngles("Body", True)
        torso_pitch = imu_data[0]  # Inclinaison avant/arrière
        torso_roll = imu_data[1]  # Inclinaison gauche/droite
        
        zmp = calculate_zmp()
        if zmp:
            zmp_x, _ = zmp
            correction_roll = -zmp_x * 0.5  # Ajuste la posture en fonction du ZMP
            motion_proxy.setAngles("LHipRoll", correction_roll, 0.1)
        
        time.sleep(0.1)
    
    # Étape 3 : Effectuer un tir avec la jambe droite
    names = ["RHipPitch", "RKneePitch", "RAnklePitch"]
    angles = [math.radians(-30), math.radians(60), math.radians(-30)]
    motion_proxy.setAngles(names, angles, 0.5)
    time.sleep(0.5)
    
    # Remettre la jambe en position initiale
    angles = [math.radians(-10), math.radians(30), math.radians(-10)]
    motion_proxy.setAngles(names, angles, 0.5)
    time.sleep(0.5)
    
    # Étape 4 : Remise en position initiale
    posture_proxy.goToPosture("StandInit", 0.5)

# Exécuter la fonction
balance_and_kick()

motion_proxy.rest()
print("NAO est maintenant au repos.")
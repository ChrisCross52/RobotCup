# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time

def courir(robot_ip, port=9559, speed=1.0, duration=5):
    
    try:
        motion_proxy = ALProxy("ALMotion", robot_ip, port)
        posture_proxy = ALProxy("ALRobotPosture", robot_ip, port)
        
        motion_proxy.wakeUp()
        
        posture_proxy.goToPosture("StandInit", 0.5)
        
        motion_proxy.moveToward(speed, 0.0, 0.0)  
        
        time.sleep(duration) 
        
        motion_proxy.stopMove()
        motion_proxy.rest()
        
    except Exception as e:
        print("Erreur de connexion ou d'exécution :", e)

if __name__ == "__main__":
    robot_ip = "192.168.0.110"  
    courir(robot_ip, speed=1.0, duration=5)

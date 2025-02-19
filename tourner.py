# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time

robot_ip = "192.168.143.30"
port = 9559

motion = ALProxy("ALMotion", robot_ip, port)

motion.wakeUp()  
motion.moveTo(0, 0, 6.28) 
motion.rest()  
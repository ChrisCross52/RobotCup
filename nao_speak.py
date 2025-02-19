# -*- coding: utf-8 -*-

from naoqi import ALProxy

if __name__ == "__main__":
    NAO_IP = "192.168.143.30" 
    NAO_PORT = 9559

tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
tts.setLanguage("French")
tts.say("Bonjour, je suis NAO !")

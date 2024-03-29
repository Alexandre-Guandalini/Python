#!/usr/bin/env python2.7
# -*- coding: utf-8 -*
import RPi.GPIO as GPIO
import time
from datetime import datetime
from PIL import Image
import pygame
from pygame.locals import *
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
width, height = screen.get_size()


def takepic(imageName): #prend une photo (note: il faut selectionner la ligne qui correspond Ã  votre installation en enlevant le premier # )
    # command = "sudo raspistill -t 1000 -w 960 -h 720 -o "+ imageName +" -q 80" #prend une photo
    # command = "sudo raspistill -t 1000 -w 960 -h 720 -o "+ imageName +" -rot 90 -q 80" #prend une photo et la tourne de 90Â°
    command = "sudo raspistill -t 1000 -w 960 -h 720 -o "+ imageName +" -rot 180 -q 80" #prend une photo et la tourne de 180Â°
    # command = "sudo raspistill -t 1000 -w 960 -h 720 -o "+ imageName +" -rot 270 -q 80" #prend une photo et la tourne de 270Â°
    os.system(command)

def loadpic(imageName): # affiche imagename
    print("loading image: " + imageName)
    background = pygame.image.load(imageName);
    background.convert_alpha()
    background = pygame.transform.scale(background,(width,height))
    screen.blit(background,(0,0),(0,0,width,height))
    pygame.display.flip()


def minuterie():
  writemessage("      3")
  time.sleep(1)
  writemessage("      2")
  time.sleep(1)
  writemessage("      1")
  time.sleep(1)
  writemessage("souriez")


def writemessage(message): # pour pouvoir afficher des messages sur un font noir 
    screen.fill(pygame.Color(0,0,0))
    font = pygame.font.SysFont("verdana", 250, bold=1)
    textsurface = font.render(message, 1, pygame.Color(255,255,255))
    screen.blit(textsurface,(35,40))
    pygame.display.update()


def writemessagetransparent(message): # pour pouvoir afficher des messages en conservant le font 
    font = pygame.font.SysFont("verdana", 50, bold=1)
    textsurface = font.render(message, 1, pygame.Color(255,255,255))
    screen.blit(textsurface,(35,40))
    pygame.display.update()



if (os.path.isdir("/home/pi/Desktop/photos") == False): # si le dossier pour stocker les photos n'existe pas       
   os.mkdir("/home/pi/Desktop/photos")                  # alors on crÃ©e le dossier (sur le bureau)
   os.chmod("/home/pi/Desktop/photos",0o777)            # et on change les droits pour pouvoir effacer des photos


while True : #boucle jusqu'a interruption
  try:
        print ("\n attente boucle")
        
        #on attend que le bouton soit pressÃ©
        GPIO.wait_for_edge(18, GPIO.FALLING)
        # on a appuyÃ© sur le bouton...


        #on lance le decompte
        minuterie()


        #on genere le nom de la photo avec heure_min_sec
        date_today = datetime.now()
        nom_image = date_today.strftime('%d_%m_%H_%M_%S')

       
        #on prend la photo
        chemin_photo = '/home/pi/Desktop/photos/'+nom_image+'.jpeg'
        takepic(chemin_photo) #on prend la photo 

        #on affiche la photo
        loadpic(chemin_photo)

        #on affiche un message
        writemessagetransparent("et voila...")

        if (GPIO.input(18) == 0): #si le bouton est encore enfoncÃ© (sont etat sera 0)
              print("bouton  appuye, je dois sortir")
              break # alors on sort du while 
 
               

  except KeyboardInterrupt:
    print ('sortie du programme!')
    raise

GPIO.cleanup()           # reinitialisation GPIO lors d'une sortie normale
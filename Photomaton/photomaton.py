#!/usr/bin/python3
# -*- coding: utf-8 -*
import RPi.GPIO as GPIO
import time
from datetime import datetime
from PIL import Image
import pygame
from pygame.locals import *
import os

GPIO.setmode(GPIO.BCM) #Attention au choix du port ; référez-vous au site https://fr.pinout.xyz/
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
width, height = screen.get_size()

pygame.mixer.init()
son = pygame.mixer.Sound('/home/pi/Photomaton/son.wav')
canal = son.play()


def PrisePhoto(NomPhoto): #prendre une photo avec Raspistill
    #command = "sudo raspistill -t 1000 -w 960 -h 540 -o "+ NomPhoto +" -q 100" #prend une photo
    command = "sudo raspistill -t 5000 -w 1200 -h 675 -o "+ NomPhoto +" -q 100" #prend une photo
    os.system(command)

def AfficherPhoto(NomPhoto): # affiche NomPhoto
    print("loading image: " + NomPhoto)
    background = pygame.image.load(NomPhoto);
    background.convert_alpha()
    background = pygame.transform.scale(background,(width,height))
    screen.blit(background,(0,0),(0,0,width,height))
    pygame.display.flip()


def decompte():
  AfficherTexte("      Attention")
  time.sleep(1)
  AfficherTexte("      Photo après")
  time.sleep(1)
  AfficherTexte("      5 secondes")
  time.sleep(1)
  AfficherTexte("      une fois que")
  time.sleep(1)
  AfficherTexte("      vous vous verrez")
  time.sleep(1)
  AfficherTexte("      Alors --> souriez")
  time.sleep(1)
  AfficherTexte("--> Photo dans 5 secondes")
  time.sleep(1)


def AfficherTexte(message): # pour pouvoir afficher des messages sur un font noir 
    screen.fill(pygame.Color(0,0,0))
    font = pygame.font.SysFont("verdana", 150, bold=1)
    textsurface = font.render(message, 1, pygame.Color(255,255,255))
    screen.blit(textsurface,(35,40))
    pygame.display.update()


def AfficherTexteTransparent(message): # pour pouvoir afficher des messages en conservant le font 
    font = pygame.font.SysFont("verdana", 100, bold=1)
    textsurface = font.render(message, 1, pygame.Color(255,255,255))
    screen.blit(textsurface,(35,40))
    pygame.display.update()


def AfficherTexteAccueil(message): # Afficher un Texte sur l'image d'accueil (ou à la place) 
    font = pygame.font.SysFont("verdana", 50, bold=1)
    textsurface = font.render(message, 1, pygame.Color(100,150,200))
    screen.blit(textsurface,(35,40))
    pygame.display.update()


if (os.path.isdir("/home/pi/Desktop/photos") == False): # si le dossier pour stocker les photos n'existe pas       
   os.mkdir("/home/pi/Desktop/photos")                  # alors on crée le dossier (sur le bureau)
   os.chmod("/home/pi/Desktop/photos",0o777)            # et on change les droits pour pouvoir effacer des photos

AfficherPhoto("/home/pi/Photomaton/accueil.png")
#AfficherTexteAccueil("Installez-vous et appuyez sur le bouton pour prendre une photo")


while True : #boucle jusqu'a interruption
  try:
        print ("\n attente boucle")
        
        #on attend que le bouton soit pressé
        GPIO.wait_for_edge(24, GPIO.FALLING)
        # on a appuyé sur le bouton...


        #on lance le décompte
        decompte()


        #on génère le nom de la photo avec heure_min_sec
        date_today = datetime.now()
        nom_image = date_today.strftime('%d_%m_%H_%M_%S')

        
        #on déclenche la prise de photo
        #chemin_photo = '/media/pi/UNTITLED/photos/'+nom_image+'.jpeg'
        chemin_photo = '/home/pi/Desktop/photos/'+nom_image+'.jpeg'
        PrisePhoto(chemin_photo) #Déclenchement de la prise de photo
        AfficherTexte("--> Merci ! <--")


        #on affiche la photo
        time.sleep(1)
        AfficherPhoto(chemin_photo)


        #on affiche un message
        AfficherTexteTransparent("OK ; voici ce qui est dans la boite ...")
        time.sleep(5) #Ajout d'un temps d'affichage afin de repartir sur l'accueil ensuite


        #on recommence en rechargeant l'écran d'accueil
        AfficherPhoto("/home/pi/Photomaton/accueil.png")
        #AfficherTexteAccueil("Installez-vous devant l'objectif et appuyez sur le bouton noir pour prendre une photo")
        pygame.mixer.init()
        son = pygame.mixer.Sound('/home/pi/Photomaton/son.wav')
        canal = son.play()


        if (GPIO.input(24) == 0): #si le bouton est encore enfoncé (son etat sera 0)
              print ("Ho ; bouton  appuyé !!! Je dois sortir ; c'est le chef qui l'a dit !")
              break # alors on sort du while 
 

  except KeyboardInterrupt:
    print ('sortie du programme!')
    raise

GPIO.cleanup()           # reinitialisation GPIO lors d'une sortie normale



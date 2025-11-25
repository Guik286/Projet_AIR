import pygame
import json
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

# Parametres graphiques :
### Taille écran :

SCREENHEIGHT = 1080
SCREENWIDTH = 1920


### Parametres graphique :

lenATB = 1080
widATB = 50

taillecase = 60

## Base de donnees de configurations
options_MM = ["New Game","Load Game","Options","Quit"]
Option_BS = ["Attaque","Déplacement","Objet","Fuite"]

### Arene de combat
Batt_Area = pygame.Rect((0,0),(5*SCREENWIDTH/8,SCREENHEIGHT))
Batt_Area.bottomright = (SCREENWIDTH,SCREENHEIGHT)

## Background arene
image_arene = pygame.image.load('states/graphics/BackgroundTitle/BGArene.png')
width = image_arene.get_width()
height = image_arene.get_height()
Image_A = pygame.transform.scale(image_arene,(1200,1080))
rectarene = Image_A.get_rect().center = (1320,540) 




## Menu et ATB
Commande_Joueur = pygame.Rect((0,0),(2*SCREENWIDTH/8,1*SCREENHEIGHT/3))
Objet_attaque = pygame.Rect((0,1*SCREENHEIGHT/3),(2*SCREENWIDTH/8,1*SCREENHEIGHT/3))
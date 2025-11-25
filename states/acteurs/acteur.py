import pygame
from settings import *
import math
import random as rd



class Acteur:
    def __init__(self,x,y,lp=10,force=0,defense=0,vit=0,PtA=0,etat="cooldown",valeur = 0):
        self.lp = 10
        self.force = force
        self.defense = defense
        self.vit = vit
        self.x = x
        self.y = y
        self.PA = PtA
        self.etat = etat
        self.etat_jeu = "menu"
        self.hit = False
        self.valeur = valeur





        ## PA ==  Points d'action
        ### position du joueur dans l'ATB
        ## Vitesse joueur
        self.dureetour = 15
        # etat du joueur dans le gameplay


        ## Cercle d'occupation de l'espace
        self.radius_pos = 60
        self.ensemble_position = []
        
        self.wait = False
        self.cout_deplacement = 300  ## cout en PA par case de deplacement
        self.chrono_action = 0
        self.Stop_Time_Active = False



        ## Position sur l'échiquier
        self.rect = pygame.Rect((x,y),(taillecase,taillecase))
        ## Position sur l'ATB
        
        self.rect_indicateur = pygame.Rect((1920/3-50,1080),(50,10))
    

    def position_occupee(self,surface):
        self.position_acteur = pygame.draw.circle(surface,pygame.Color("white"),self.rect.center,self.radius_pos)
        self.ensemble_position.append(self.position_acteur)


    def la_place_est_prise(self):
        pass

    def mort(self):
        if self.lp <=0 :
            self.lp = 0
            self.etat = "mort"

 

    def calcul_temps_ref(self,dt):
        if not self.Stop_Time_Active:
            self.chrono_action += dt
        if self.chrono_action >= self.dureetour:
            self.chrono_action = 0

    def ordonnee_indicateur(self):
        longueur = lenATB * self.chrono_action / self.dureetour
        y = (-1) * (longueur - lenATB)
        
        self.rect_indicateur.y = y

    def deplacement(self):
        pass




    def depense_PA(self,cout):
        self.PA -= cout
        if self.PA <0 :
            self.PA =0
        if cout > self.PA:
            action = "Pas assez de PA"
        if cout <= self.PA:
            action = "Lancer l'action"
            
        return action
    


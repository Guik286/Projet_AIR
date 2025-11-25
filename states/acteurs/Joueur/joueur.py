import pygame
from settings import *
from .Attaque_joueur import *
from ..acteur import Acteur



 
class Joueur(Acteur):
    def __init__(self,x=720,y=0,lp = 30000,force = 0,defense = 0,vit = 0,PtA = 0,etat = "cooldown",valeur = 1):
        super(Joueur,self).__init__(x,y,lp,force,defense,vit,PtA,etat,valeur)
        self.experience = 0 
        self.curseur = pygame.Rect((self.x,self.y),(taillecase,taillecase))
        self.etat_jeu = "menu"
        self.dureetour = 4
        self.menuBattScreen = ["menu","attaque","map","objet","fuite"]
        #self.Attaque = ["Coup de boobs", "Mawashidantagwl","pause clope"]

        #for attaque in self.Attaque_set:
#
        #    self.Attaque.append(attaque["Nom"])
        #

        self.Attaque_index = 0
        self.Attaque = Attaque_joueur("states/data/Skill.json")
        self.signal_act = False

        ## Valeur dans la matrice 
        self.valeur = 1
        
        




    def calcul_temps_acteur(self,ref,dt):
    ### Création d'un seuil entre 2 états (casting/jouable) pour geler le temps a la fin du temps de jeu, et ne pas perdre l'action du joueur
        seuil = 5 * self.dureetour / 6.0
        if self.wait == False and self.etat != "casting":
            self.chrono_action += dt
        elif self.wait == False and self.etat == "casting":
            self.chrono_action +=  dt * self.dureetour / ref
        else:
            if self.etat_jeu == "menu" and self.chrono_action < seuil:
                self.chrono_action += dt
        if self.chrono_action >= self.dureetour:
            self.chrono_action = 0
        elif self.chrono_action > seuil and self.etat == "jouable":
            self.wait = True
        elif self.chrono_action > self.dureetour / 6.0 and self.chrono_action <= seuil:
            self.etat = "jouable"
        elif self.chrono_action <= self.dureetour / 6.0:
            self.etat = "cooldown"

        


        self.rect_indicateur = pygame.Rect((1920/3-50,1080),(50,10))

    def afficher_deplacement_possible(self,surface):
        PA = self.PA
        max_case = PA // self.cout_deplacement
        origine = (self.rect.x - 720)//taillecase , (self.rect.y)//taillecase
        for i in range(-max_case, max_case + 1):
            for j in range(-max_case, max_case + 1):
                if abs(i) + abs(j) <= max_case:
                    x = origine[0] + i
                    y = origine[1] + j
                    if 0 <= x < 20 and 0 <= y < 18:
                        rect = pygame.Rect(720 + x * taillecase, y * taillecase, taillecase, taillecase)
                        pygame.draw.rect(surface, pygame.Color("gray"), rect, 3)




    # Evenement MAP
   
    ### Evenement attaque

    #def Attaque_joueur(self,Attaque_index,cible):

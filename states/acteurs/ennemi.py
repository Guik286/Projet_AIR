#import pygame
from settings import * 
from .acteur import Acteur
import random as rd





class Ennemi(Acteur):
    def __init__(self,x,y):
        super(Ennemi,self).__init__(x,y,0,1,0,0,0,"cooldown",2)
        ## Vitesse joueur
        self.dureetour = 5
        # etat du joueur dans le gameplay
        self.rect_indicateur = pygame.Rect((1920/3-50,1080),(50,10))
        self.image = pygame.image.load('states/graphics/character/panther.png')
        self.rect_img = self.image.get_rect()
        self.rect_img.center = self.rect.center
        self.image_hit = pygame.image.load('states/graphics/character/panther_hit.png')
        self.rect_hit = self.image_hit.get_rect()
        self.rect_hit.center = self.rect.center


        
        



    def calcul_temps_acteur(self,ref,dt):
    ### Création d'un seuil entre 2 états (casting/jouable) pour geler le temps a la fin du temps de jeu, et ne pas perdre l'action du joueur
        seuil = 5 * self.dureetour / 6.0
        if self.wait:
            pass
        elif self.wait == False and self.etat != "casting":
            self.chrono_action += dt
        elif self.wait == False and self.etat == "casting":
            self.chrono_action +=  dt * self.dureetour / ref
        else:
            if  self.etat_jeu == "menu" and self.chrono_action < seuil:
                self.chrono_action += dt
        if self.chrono_action >= self.dureetour:
            self.chrono_action = 0
        elif self.chrono_action > seuil and self.etat == "jouable":
            self.wait = True
        elif self.chrono_action > self.dureetour / 6.0 and self.chrono_action <= seuil:
            self.etat = "jouable"
        elif self.chrono_action <= self.dureetour / 6.0:
            self.etat = "cooldown"




    #### Méthodes ennemis ####
    def Calcul_PA(self):
        self.PA = round(2 * self.chrono_action*1080 / self.dureetour)



    def deplacement_ennemi(self,cible):
        self.Calcul_PA()

        if self.PA >= self.cout_deplacement:
            if self.rect.x < cible.rect.x:
                self.rect.x += taillecase * self.PA//self.cout_deplacement
            elif self.rect.x > cible.rect.x:
                self.rect.x -= taillecase * self.PA//self.cout_deplacement
            if self.rect.y < cible.rect.y:
                self.rect.y += taillecase * self.PA//self.cout_deplacement
            elif self.rect.y > cible.rect.y:
                self.rect.y -= taillecase * self.PA//self.cout_deplacement
            self.rect_img.x, self.rect_img.y = self.rect.x, self.rect.y
            
    
    

    def Action_ennemi(self,cible):
        self.Calcul_PA()
        # Exemple d'action simple : attaquer la cible
        if self.PA >= 500:
            damage = max(0, self.force - cible.defense)
            cible.lp -= damage
            print(f"L'ennemi attaque et inflige {damage} points de dégâts !")
            print(f"{cible} a pris 1 point de dégats")
            print(f"{cible} a {cible.lp}")

 
    
    def IA_ennemi(self,cible):
        # Simple IA : se déplace vers le joueur et attaque s'il est à portée
        distance_x = abs(self.rect.x - cible.rect.x)
        distance_y = abs(self.rect.y - cible.rect.y)

        if distance_x > taillecase and distance_y > taillecase:

            self.deplacement_ennemi(cible)
            
        else:
            self.Calcul_PA()
            self.Action_ennemi(cible)
            
        self.chrono_action = 5* self.dureetour/6
        self.wait = False
        self.etat = "casting"

    def flash_on_hit(self):
        if self.hit ==True:
            self.rect_img = self.image_hit

        

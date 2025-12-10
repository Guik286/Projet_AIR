import pygame
from Data.settings import * 
from .acteur import Acteur
import random as rd
from math import sqrt





class Ennemi(Acteur):
    def __init__(self,x,y):
        super(Ennemi,self).__init__(x,y,10,1,0,0,0,"cooldown",2)
        ## Vitesse joueur
        self.dureetour = 8
        # etat du joueur dans le gameplay
        self.rect_indicateur = pygame.Rect((1920/3-50,1080),(50,10))
        self.image_hit()
        self.rect_img = self.image.get_rect()
        self.rect_img.center = self.rect.center


    def image_hit(self):
        if self.hit > 0:
            self.image = pygame.image.load('Data/graphics/character/panther_hit.png')
        else:
            self.image = pygame.image.load('Data/graphics/character/panther.png')

        
        



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



    def deplacement_ennemi(self,cible,grid):
        self.Calcul_PA()


        if self.PA >= self.cout_deplacement:
            x = self.x
            y = self.y

            if self.x < cible.x and grid[self.x +1][self.y] is None:
                self.x +=1
            elif self.x > cible.x and grid[self.x -1][self.y] is None:
                self.x -= 1
            if self.y < cible.y and grid[self.x][self.y +1] is None:
                self.y += 1
            elif self.y > cible.y and grid[self.x][self.y -1] is None:
                self.y -= 1
            

            
            
            self.rect.x,self.rect.y = 720 + self.x * taillecase,self.y * taillecase
            
            if self.x != x and self.y != y:
                self.PA -= self.cout_deplacement_diag

            else:
                self.PA -= self.cout_deplacement

            print(f"L'ennemi se déplace en ({self.x},{self.y})")
            self.rect_img.center = self.rect.center
            
            
    
    

    def Action_ennemi(self,cible):
        self.Calcul_PA()
        # Exemple d'action simple : attaquer la cible
        if self.PA >= 500:
            damage = max(0, self.force - cible.defense)
            cible.lp -= damage
            print(f"L'ennemi attaque et inflige {damage} points de dégâts !")
            print(cible.lp)
            #print(f"{cible} a pris 1 point de dégats")
            #print(f"{cible} a {cible.lp}")

 
    
    def IA_ennemi(self,cible,grid):
        # Simple IA : se déplace vers le joueur et attaque s'il est à portée
        

        if sqrt((self.x - cible.x)**2 + (self.y - cible.y)**2) > sqrt(2):

            self.deplacement_ennemi(cible,grid)
            
        else:
            self.Calcul_PA()
            self.Action_ennemi(cible)
            
        self.chrono_action = 5* self.dureetour/6
        self.wait = False
        self.etat = "casting"

    def flash_on_hit(self):
        if self.hit ==True:
            self.rect_img = self.image_hit
            

        

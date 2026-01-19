import pygame
from Data.settings import * 
from .acteur import Acteur
import random as rd
from math import sqrt





class Ennemi(Acteur):
    def __init__(self,x,y):
        super(Ennemi,self).__init__(x,y,10,1,0,0,0,1500)
        ## Vitesse joueur
        self.temps_tot = 8
        # etat du joueur dans le gameplay
        self.rect_indicateur = pygame.Rect((1920/3-50,1080),(50,10))
        self.image_hit()
        self.rect_img = self.image.get_rect()
        self.rect_img.center = self.rect.center
        self.action = 0
        self.action_threshold = 0
        self.etat_precedent = self.etat
        self.threshold_generated = False
        self.Etats[1]["modif"] = 5


    def image_hit(self):
        if self.hit > 0:
            self.image = pygame.image.load('Data/graphics/character/panther_hit.png')
        else:
            self.image = pygame.image.load('Data/graphics/character/panther.png')

        
        



    def calcul_temps_acteur(self,dt):
    ### Création d'un seuil entre 2 états (casting/jouable) pour geler le temps a la fin du temps de jeu, et ne pas perdre l'action du joueur

        self.calcul_temps_ref(dt)
        self.PA = self.chrono * 150

        if self.etat["nom"] == "cooldown" and not self.threshold_generated:
            self.action_threshold = rd.randint(5,9) * self.PA_max / 10
            self.threshold_generated = True
        elif self.etat["nom"] != "cooldown":
            self.threshold_generated = False

        #if self.chrono == 0 and self.etat["nom"] == "cooldown":
            ## on calcule une borne de PA à partir de laquellle il agit
            








    def deplacement_ennemi(self,cible,grid):
        


        while self.PA >= self.cout_deplacement:
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
            
            

            
            self.deplacement_acteur(self.x,self.y)
            
            #self.rect.x,self.rect.y = 720 + self.x * taillecase,self.y * taillecase
            
            if self.x != x and self.y != y:
                self.PA -= self.cout_deplacement_diag

            else:
                self.PA -= self.cout_deplacement
            
            print(f"L'ennemi se déplace en ({self.x},{self.y})")
        self.reset_to_cooldown()

            
            
    
    

    def Attaque_ennemi(self,cible):
        # Exemple d'action simple : attaquer la cible
        if self.PA >= 500:
            damage = max(0, self.force - cible.defense)
            cible.lp -= damage
            print(f"L'ennemi attaque et inflige {damage} points de dégâts !")
            print(cible.lp)

 
    
    def IA_ennemi(self,cible,grid):
        # Simple IA : se déplace vers le joueur et attaque s'il est à portée
        ## On met à jour les PA de l'ennemi
        

        ## On détermine une limite à partir de laquelle l'ennemi agit
        #limite = self.PA_max*rd.randint(1000,5000)/5000
        if self.PA < self.action_threshold:
            pass
        else:
        

            if sqrt((self.x - cible.x)**2 + (self.y - cible.y)**2) > sqrt(2):

                self.deplacement_ennemi(cible,grid)
                

            else:

                self.Attaque_ennemi(cible)
                self.wait = False
                self.etat = self.Etats[self.index_etat+1]
            
            
            
        

    def flash_on_hit(self):
        if self.hit ==True:
            self.rect_img = self.image_hit
            

        

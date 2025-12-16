import pygame
from Data.settings import * 
from .acteur import Acteur
import random as rd
from math import sqrt





class Ennemi(Acteur):
    def __init__(self,x,y):
        super(Ennemi,self).__init__(x,y,10,1,0,0,0,2,3000)
        ## Vitesse joueur
        self.temps_tot = 8
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

        
        



    def calcul_temps_acteur(self,dt):
    ### Création d'un seuil entre 2 états (casting/jouable) pour geler le temps a la fin du temps de jeu, et ne pas perdre l'action du joueur
        if self.etat is not "cooldown":
            pass
        else:
            self.calcul_temps_ref(dt)





    #### Méthodes ennemis ####
    def Calcul_PA(self):
        self.PA = round(self.PA_max * self.chrono*5 / 2)




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
            

            
            self.deplacement_acteur(self.x,self.y)
            #self.rect.x,self.rect.y = 720 + self.x * taillecase,self.y * taillecase
            
            if self.x != x and self.y != y:
                self.PA -= self.cout_deplacement_diag

            else:
                self.PA -= self.cout_deplacement

            print(f"L'ennemi se déplace en ({self.x},{self.y})")

            
            
    
    

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
        ## On met à jour les PA de l'ennemi
        self.Calcul_PA()

        ## On détermine une limite à partir de laquelle l'ennemi agit
        limite = self.PA_max*rd.randint(1000,5000)/5000
        if self.PA < limite:
            pass
        else:
        

            if sqrt((self.x - cible.x)**2 + (self.y - cible.y)**2) > sqrt(2):

                self.deplacement_ennemi(cible,grid)

            else:

                self.Action_ennemi(cible)
            
            self.chrono = 200
            self.wait = False
            self.etat = "casting"
        

    def flash_on_hit(self):
        if self.hit ==True:
            self.rect_img = self.image_hit
            

        

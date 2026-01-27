from math import sqrt
import pygame
from settingsBrouillonBS import *


class EffetSpatiaux:
    ##### Effet de déplacement d'un point sur la matrice
    def __init__(self,Matrice):
        self.matrice = Matrice

    def Knockback(self,cible,source):
        ### Direction 
        direction = ((cible.x - source.x),(cible.y-source.y))
        if direction[0] != 0:
            newx = cible.x + int(direction[0]/sqrt((cible.x-source.x)**2 ))
        else:
            newx = cible.x
        if direction[1] !=0 : 

            newy = cible.y + int(direction[1]/sqrt((cible.y-source.y)**2))
        else:
            newy = cible.y

        self.matrice.deplacer_element(cible,newx,newy)
        cible.x = newx
        cible.y = newy
        #self.EnnemiRectangle = pygame.Rect(cible.x * taillecol, cible.y * taillerow, taillecol, taillerow)

    def Mouvement(self,point,cible):
        path = self.matrice.pathfinding(point,cible)
        


        
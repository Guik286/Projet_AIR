import pygame

from Game_f.states.base import BaseState
from Game_f.states.acteurs.acteur import Acteur
from Game_f.states.acteurs.Joueur.joueur import Joueur
from Game_f.states.acteurs.ennemi import Ennemi
from GI import GraphicInterface

import random as rd


from Data.settings import taillecase


class Matrice_Bagarre:
    def __init__(self):

        #On creer un échiquier (matrice pleine de zero)

        self.echiquier = [[0 for i in range(0,18)] for j in range(0,20)]

        ## 1 : joueur , 2 : ennemi

        ## Test placement aléatoire acteurs
        self.player = Joueur(rd.randint(0,5),rd.randint(0,5))
        self.ennemi = Ennemi(rd.randint(15,19),rd.randint(14,17))
        self.ennemi2 = Ennemi(rd.randint(15,19),rd.randint(14,17))
        
        self.Acteurs = {"Nom dictionnaire" : "Acteurs" , "Joueurs" :[self.player] , "Ennemis" : [self.ennemi,self.ennemi2] }
        self.ref = Acteur(0,0)


        self.echiquier[self.player.x][self.player.y] = self.player.valeur
        for Ennemis in self.Acteurs["Ennemis"]:
            self.echiquier[Ennemis.x][Ennemis.y] = Ennemis.valeur
            



    def Deplacement(self,acteur,xcible,ycible):
        #position initiale de l'acteur : 
        xact, yact = acteur.x, acteur.y
        self.echiquier[xact,yact] = 0
        self.echiquier[xcible,ycible] = acteur.valeur

    def position_map(self,acteur):
        acteur.x = 720 + acteur.x * taillecase 
        acteur.y = acteur.y * taillecase
        return (acteur.x,acteur.y)



Matrice_Bagarre()
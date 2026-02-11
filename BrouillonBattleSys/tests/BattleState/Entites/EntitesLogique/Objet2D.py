import pygame
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from BrouillonBattleSys.settingsBrouillonBS import *
from .Point2D import Point2D
from BrouillonBattleSys.tests.BattleState.BattleSysteme import Gestion_Acteur as GA
from BrouillonBattleSys.tests.BattleState.BattleSysteme import GraphObjet as GO
from settingsBrouillonBS import *








## Classe fille des points, un objet est un point avec des propriétés supplémentaires
class objet2D(Point2D):
    ### Classe fille de point2D, un objet est un point avec des propriétés supplémentaires
    def __init__(self, x, y, nom = "Objet", description = "", lp_max = 10,defense = 1,Etat = "no_alt",Image=None):
        super(objet2D,self).__init__(x, y)
        self.nom = nom
        self.description = description
        #Statistiques de l'objet
        self.lp_max = lp_max
        self.lp = lp_max
        self.defense = defense
        #Image et rectangle de l'objet
        self.image = Image
        self.rect = pygame.Rect(x,y,taillerow,taillecol)
        self.rect_img = None
        if self.image is not None:
            self.rect_img = self.image.get_rect()
            self.rect_img.center = self.rect.center
        self.Etat = Etat  # Etat de l'objet (ex: "no_alt", "altéré", "cassé", etc.)
        self.hit = False

        ### Temps 

        self.horloge = 0  ### Horloge interne pour les actions temporelles



    def mort(self):
        if self.lp <= 0:
            self.lp = 0
            self.Etat = "mort"
            print(f"{self.nom} est mort.")
            

    def Recevoir_degats(self, degats):
        self.lp -= degats
        print(f"{self.nom} a reçu {degats} points de dégâts. Points de vie restants : {self.lp}")
        if self.lp <= 0:
            self.mort()
        # Actions supplémentaires à la mort de l'objet peuvent être ajoutées ici

### Classe fille des objets, un acteur est un objet avec des statistiques de combat

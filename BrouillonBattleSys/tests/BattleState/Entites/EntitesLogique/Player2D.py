import pygame
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from BrouillonBattleSys.settingsBrouillonBS import *
from .Point2D import Point2D
from .Objet2D import objet2D
from BrouillonBattleSys.tests.BattleState.BattleSysteme import Gestion_Acteur as GA
from BrouillonBattleSys.tests.BattleState.BattleSysteme import GraphObjet as GO
from settingsBrouillonBS import *

from .Timer import Timer




class Acteur(objet2D):
    def __init__(self, x, y, nom ="Acteur", description = "", lp=100, defense=10,Etat = "no_alt",Image=None, FORCE = 1, vit = 1,PA_max=20):
        super(Acteur,self).__init__(x, y,nom = "Acteur", description="")
        self.nom = nom
        self.description = description
        self.lp = lp
        self.defense = defense
        self.FORCE = FORCE
        self.atq = FORCE * 2
        self.vit = vit
        self.image = Image
        self.Etat = Etat
        self.rect = pygame.Rect(x,y,taillerow,taillecol)
        self.initiative = 0
        self.PA_max = PA_max
        self.PA = 0

        ###Variable temporelle
        self.Barre_action = Timer(5000)  ### 5 secondes pour se préparer à agir
        self.Barre_resolution = Timer(5000)  ### 5 secondes pour résoudre l'action
        self.horloge_action = 0
        self.horloge_resolution = 0
        self.pause_action = False
        self.pause_resolution = True

         ### L'acteur commence à générer des PA dès le début du combat

    #### A encapsuler plus tard , Logique des horloges

    ### Etape 1: une horloge interrompable à chaque instant, les PA se generent et on peut acceder aux options

    def Action(self):
        self.Barre_action.activer()  ### Activer la barre d'action au début de la phase d'action
        self.Barre_action.update()
        print(self.Barre_action.current_time)
        if self.Barre_action.__bool__(): # Ou quand le joueur appuie sur un bouton
            pass
        else:
            print(f"{self.nom} est prêt à agir.")
            self.Resolution()  ### Commencer la phase de résolution

    def Resolution(self):
        self.Barre_resolution.activer()  ### Activer la barre de résolution au début de la phase de résolution
        self.Barre_resolution.update()
        if self.Barre_resolution.__bool__():
            pass
        else:
            print(f"{self.nom} a résolu son action.")
            self.Action()  ### Recommencer la phase d'action pour le prochain tour

    #### Les PA se generent au cours du temps, on va creer un essai simple



    def IA_Ennemi(self,dt,grillelogique,deplalogique,cible):
        ### IA simple pour l'ennemi : se déplace vers le joueur et attaque s'il est à portée

        self.Action()

        self.Resolution()
        print(f" Horloge de résolution : {self.horloge_resolution}")
        if self.pause_action and self.Etat != "mort":

            print(f"L'ennemi a {self.PA} PA, il peut agir.")
            self.pause_action = True
            self.pause_resolution = False
            

            path_ennemi = grillelogique.pathfinding(self,cible)
            if path_ennemi is not None and len(path_ennemi) > 2 and self.horloge_action >= 0:
                print("L'ennemi se déplace vers le joueur.")
                i = 0
                ###Mettre une boucle autorisant un déplacement sur plusieurs cases si PA le permet
                ## conditionner la boucle à l'horloge de résolution pour faire évoluer l'ennemi sur le chemin pendant la phase de résolution
                if self.horloge_resolution <= 5:  ## On peut faire évoluer l'ennemi sur le chemin pendant la phase de résolution
                    if self.horloge_resolution <= i*60:
                        pass
                    else:
                        i += 1
                        deplalogique.Mouvement(self,len(path_ennemi)-(1+i),path_ennemi)
                        GO(self).rectangle = pygame.Rect(self.x * taillecol, self.y * taillerow, taillecol, taillerow)
                        self.horloge_action -= 5
                        print(f"PA restant : {self.horloge_action}")
                else: # Fin résolution
                    self.pause_resolution = True
                    self.horloge_resolution = 0
                    self.pause_action = False
                    self.horloge_action = 0
                
            elif path_ennemi is not None and len(path_ennemi) == 2:
                print("L'ennemi attaque le joueur.")
                GA(self,grillelogique).attaque(cible)
                self.horloge_action -= 50
                self.pause_resolution = True
                self.horloge_resolution = 0
                self.pause_action = False
                self.horloge_action = 0
            else:
                print("L'ennemi ne peut pas atteindre le joueur cette fois-ci.")
                self.pause_resolution = True
                self.horloge_resolution = 0
                self.pause_action = False
                self.horloge_action = 0



        


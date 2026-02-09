import pygame
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Data.settings import *
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
        self.rect = pygame.Rect(x,y,taillecase,taillecase)
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
        self.rect = pygame.Rect(x,y,taillecase,taillecase)
        self.initiative = 0
        self.PA_max = PA_max
        self.PA = 0

        ###Variable temporelle
        self.horloge_action = 0
        self.horloge_resolution = 0
        self.pause_action = False
        self.pause_resolution = True

    #### A encapsuler plus tard , Logique des horloges

    ### Etape 1: une horloge interrompable à chaque instant, les PA se generent et on peut acceder aux options

    def Barre_action(self,dt):
        if not self.pause_action: # Ou quand le joueur appuie sur un bouton
            self.horloge_action += dt
            if self.horloge_action > 5:  ### 1 secondes ou un temps de pause.
                self.pause_action = True
                print(f"{self.nom} peut agir maintenant.")

    def Barre_resolution(self,dt):
        if not self.pause_resolution:
            self.horloge_resolution += dt
            if self.horloge_resolution > 200:  ### 1 secondes
                self.pause_resolution = True
                self.horloge_resolution = 0
                print(f"{self.nom} a résolu son action.")

    #### Les PA se generent au cours du temps, on va creer un essai simple
    def generer_PA(self):
        if self.PA > self.PA_max:
            self.PA = self.PA_max
        
        self.PA =  self.horloge_action  ### 5 PA par seconde
        if int(self.PA) // 10 == 1:
            pass
            #print(f"{self.nom} a {self.PA} PA, il doit attendre pour agir.")


    def IA_Ennemi(self,dt,grillelogique,deplalogique,cible):
        ### IA simple pour l'ennemi : se déplace vers le joueur et attaque s'il est à portée

        self.Barre_action(dt)
        self.generer_PA()
        self.Barre_resolution(dt)
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
                if self.horloge_resolution <= 250:  ## On peut faire évoluer l'ennemi sur le chemin pendant la phase de résolution
                    if self.horloge_resolution <= i*100:
                        pass
                    else:
                        i += 1
                        deplalogique.Mouvement(self,len(path_ennemi)-(1+i),path_ennemi)
                        GO(self).rectangle = pygame.Rect(self.x * taillecol, self.y * taillerow, taillecol, taillerow)
                        self.horloge_action -= 10
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



        


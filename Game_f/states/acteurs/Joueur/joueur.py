import pygame
from Data.settings import *
from .Attaque_joueur import *
from ..acteur import Acteur
from math import sqrt



 
class Joueur(Acteur):
    def __init__(self,x=0,y=0,lp = 300,force = 0,defense = 0,vit = 0,PtA = 0, PA_max = 100):
        super(Joueur,self).__init__(x,y,lp,force,defense,vit,PtA,PA_max)
        self.experience = 0 
        self.curseur = pygame.Rect((self.x,self.y),(taillecase,taillecase))
        self.etat_jeu = "menu"
        self.menuBattScreen = ["menu","attaque","map","objet","fuite"]
        #self.Attaque = ["Coup de boobs", "Mawashidantagwl","pause clope"]

        #for attaque in self.Attaque_set:
#
        #    self.Attaque.append(attaque["Nom"])
        #

        self.Attaque_index = 0
        self.Attaque = Attaque_joueur()
        self.signal_act = False
        self.charge = False

        self.etat_precedent = self.Etats[self.index_etat]
        self.etat = self.etat_precedent
        
        self.Etats[1]["modif"] = 5

        ## Valeur dans la matrice 

        
        




    def calcul_temps_acteur(self,dt):
    ### Création d'un seuil entre 2 états (casting/jouable) pour geler le temps a la fin du temps de jeu, et ne pas perdre l'action du joueur
        self.calcul_temps_ref(dt)
        if self.etat_precedent["nom"] == "cooldown":
            self.signal_act = False


        if self.etat_precedent["nom"] != "casting":
            
            self.PA = self.chrono * 100
        else:
            pass
        self.stop_before_casting()
            



        


        self.rect_indicateur = pygame.Rect((1920/3-50,1080),(50,10))

    def stop_before_casting(self):
        if self.Etats[self.index_etat]["nom"] is not "casting":
            self.etat_precedent = self.Etats[self.index_etat]
        else:
            if not self.signal_act:
                self.wait = True
                self.PA = self.PA_max

            else:
                pass



    def afficher_deplacement_possible(self,surface,grid):
        PA = self.PA
        max_case = int(PA // self.cout_deplacement)
        

        origine = (self.rect.x - 720)//taillecase , (self.rect.y)//taillecase
        
        for i in range(-max_case, max_case + 1):
            for j in range(-max_case, max_case + 1):
                D = sqrt(abs(i)**2 + abs(j)**2)
                if D < max_case:
                    x = origine[0] + i
                    y = origine[1] + j
                    if 0 <= x < 20 and 0 <= y < 18 and grid[x][y] is None:
                        grid[x][y] = "possible"
                    if grid[x][y] == "possible":
                        rect = pygame.Rect(720 + x * taillecase, y * taillecase, taillecase, taillecase)
                        pygame.draw.rect(surface, pygame.Color("gray"), rect, 3)
        
        



    # Evenement MAP
   
    ### Evenement attaque

    #def Attaque_joueur(self,Attaque_index,cible):

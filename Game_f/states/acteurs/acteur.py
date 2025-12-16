import pygame
from Data.settings import *
from math import sqrt
import random as rd



class Acteur:
    def __init__(self,x,y,lp=10,force=0,defense=0,vit=0,PtA=0,PA_max=0):

        # Statistique de base
        self.lp = lp
        self.lp_max = lp
        self.force = force
        self.defense = defense
        self.vit = vit
        self.x = x
        self.y = y
        self.PA = PtA
        self.etat_jeu = "menu"
        self.hit = 0
        self.damage = 0
        self.PA_max = PA_max
        if self.PA > self.PA_max:
            self.PA = self.PA_max

        ### Image de l'acteur ###
        self.image = None
        if self.image is not None:
            self.rect_img = self.image.get_rect()
            self.rect_img.center = self.rect.center

      ### Coordonnées sur la matrice ####

        

        self.grid_pos = (self.x,self.y)






        ## PA ==  Points d'action
        ### position du joueur dans l'ATB
        ## Vitesse joueur
        
        # etat du joueur dans le gameplay


        ## Cercle d'occupation de l'espace

        
        self.wait = False
        self.cout_deplacement = 300
        self.cout_deplacement_diag = sqrt(2) * self.cout_deplacement  ## cout en PA par case de deplacement

        #### Tout les temps et chronos ####

        ### Dictionnaire des états possibles :
        # "cooldown" : temps de recharge avant de pouvoir agir 
        # "jouable" : temps durant lequel le joueur peut agir
        # "casting" : temps durant lequel l'action est en cours d'execution
        # "action" : temps durant lequel l'action s'execute
        # "mort" : acteur mort, plus d'action possible
        self.Etats = [{"nom" : "cooldown", "modif" : 1, "tps_max" : 2,"long" : 1/6, "origine" : lenATB},
                      {"nom" : "jouable", "modif" : 1, "tps_max" : 10, "long" : 4/6, "origine" : 5*lenATB/6},
                      {"nom" : "casting", "modif" : 1, "tps_max" : 1, "long" : 1/6, "origine" : lenATB/6}] #,"trigger" : self.casting()}]
        self.index_etat = 0
        self.Etat_mort = [{"nom" : "mort", "modif" : 0, "tps_max" : 0,"long" : 0, "origine" : 0}]
        self.etat = self.Etats[self.index_etat]

        self.chrono = 0
        
        

        ## Position sur l'échiquier

        self.rect = pygame.Rect((720 + x * taillecase,y * taillecase),(taillecase,taillecase))
        ## Position sur l'ATB
        
        self.rect_indicateur = pygame.Rect((1920/3-50,1080),(50,10))



        #### Dictionnaires des animations ####
        self.animations = {}
        
    
############# Etat #####################################

    def Etat_suivant(self):
        if self.chrono >= self.etat["tps_max"]  :
            self.chrono = 0
            next_index = self.index_etat +1
            if next_index >= len(self.Etats):
                next_index = 0
            self.index_etat = next_index
            self.etat = self.Etats[next_index]
                

            

    def mort(self):
        if self.lp <=0 :
            self.lp = 0
            self.etat = self.Etat_mort

    def get_striked(self,striker,skill):
        if self.hit <1 :
            pass
        else:
            self.hit = 15
            self.image_hit()
            ## animation du hit
            ## application des dégats
            ## application du knockback
            if not skill["KB"] >0:
                pass
            else:
                origin = striker.rect.center
                power = skill["KB"]
                self.knockback(origin,power)
            #    self.rect_img.center = self.rect.center


            ## application des effets secondaires

            




################ Temporel #####################################

    def calcul_temps_ref(self,dt):
        
        
        ## Si un signal stop, le temps de l'acteur s'arrête
        if self.wait:
            pass
        ## Si on est durant le cooldown
        else:
            self.chrono += dt * self.etat["modif"] #(*une variable de contingence)
        self.Etat_suivant()





    def ordonnee_indicateur(self):
        longueur = self.etat["long"] * lenATB * self.chrono / self.etat["tps_max"]
        y = self.etat["origine"] + (-1) * (longueur - self.etat["long"])
        
        self.rect_indicateur.y = y





################ Spatial ############################## 

    def deplacement_acteur(self,new_x,new_y):
        if new_x <0 :
            new_x =0
        if new_y <0 :
            new_y =0
        if new_x >ncol -1:
            new_x = ncol -1
        if new_y >nrow -1:
            new_y = nrow -1
        
        self.x = new_x
        self.y = new_y
        self.rect.topleft = (720 + taillecase *self.x,taillecase *self.y)
        if self.image is not None:
            self.rect_img.center = self.rect.center





    def depense_PA(self,cout):
        self.PA -= cout
        if self.PA <0 :
            self.PA =0
        if cout > self.PA:
            action = "Pas assez de PA"
        if cout <= self.PA:
            action = "Lancer l'action"
            
        return action
    
    def knockback(self,origin,power):

        self.grid_pos = (self.x,self.y)


        # Position de l'attaquant
        pos_attaquant = pygame.math.Vector2(origin)
        # Position de la cible
        pos_cible = pygame.math.Vector2(self.rect.center)
        # Calcul du vecteur de knockback (direction de la poussée)
        direction = pos_cible - pos_attaquant
        if direction.length() != 0:  # Évite la division par zéro
            direction = direction.normalize()
        knockback_distance = power 
        nouvelle_pos = self.grid_pos + direction * knockback_distance
        # Appliquer le déplacement logique
        self.deplacement_acteur(round(nouvelle_pos.x),round(nouvelle_pos.y))

        ## Synchronisation avec le visuel 
        #self.rect.topleft = (720 + taillecase *self.x,taillecase *self.y)
        #
        ## --- Synchroniser la position logique (si présente) ---
        ## Exemple : si l'acteur garde des coordonnées de case (case_x, case_y)
        #if hasattr(self.cible, "case_x") and hasattr(self.cible, "case_y"):
        #    # convertir pixels -> indices de case (ajuster offset / taille si différent)
        #    self.cible.case_x = int((self.cible.rect.x - 720) // taillecase)
        #    self.cible.case_y = int(self.cible.rect.y // taillecase)
        ## Exemple : attribut générique grid_pos = (x,y)
        #elif hasattr(self.cible, "grid_pos"):
        #    print(hasattr(self.cible, "grid_pos"))
        #    gx = int((self.cible.rect.x - 720) // taillecase)
        #    gy = int(self.cible.rect.y // taillecase)
        #    self.cible.grid_pos = (gx, gy)
        #    print(gx,gy)
        ## Sinon, stocker la nouvelle position comme position source pour éviter override
        #else:
        #    self.cible.base_pos = (self.cible.rect.x, self.cible.rect.y)





    


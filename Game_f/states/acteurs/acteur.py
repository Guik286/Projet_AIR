import pygame
from Data.settings import *
from math import sqrt
import random as rd



class Acteur:
    def __init__(self,x,y,lp=10,force=0,defense=0,vit=0,PtA=0,etat="cooldown",valeur = 0,PA_max=0):

        # Statistique de base
        self.lp = lp
        self.lp_max = lp
        self.force = force
        self.defense = defense
        self.vit = vit
        self.x = x
        self.y = y
        self.PA = PtA
        self.etat = etat
        self.etat_jeu = "menu"
        self.hit = 0
        self.valeur = valeur
        self.damage = 0
        self.PA_max = PA_max
        if self.PA > self.PA_max:
            self.PA = self.PA_max

      ### Coordonnées sur la matrice ####

        

        self.grid_pos = (self.x,self.y)






        ## PA ==  Points d'action
        ### position du joueur dans l'ATB
        ## Vitesse joueur
        self.dureetour = 15
        # etat du joueur dans le gameplay


        ## Cercle d'occupation de l'espace

        
        self.wait = False
        self.cout_deplacement = 300
        self.cout_deplacement_diag = sqrt(2) * self.cout_deplacement  ## cout en PA par case de deplacement
        self.chrono_action = 0
        self.Stop_Time_Active = False



        ## Position sur l'échiquier

        self.rect = pygame.Rect((720 + x * taillecase,y * taillecase),(taillecase,taillecase))
        ## Position sur l'ATB
        
        self.rect_indicateur = pygame.Rect((1920/3-50,1080),(50,10))



        #### Dictionnaires des animations ####
        self.animations = {}
        
    
############# Etat #####################################


    def mort(self):
        if self.lp <=0 :
            self.lp = 0
            self.etat = "mort"

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
        if not self.Stop_Time_Active:
            self.chrono_action += dt
        if self.chrono_action >= self.dureetour:
            self.chrono_action = 0

    def ordonnee_indicateur(self):
        longueur = lenATB * self.chrono_action / self.dureetour
        y = (-1) * (longueur - lenATB)
        
        self.rect_indicateur.y = y

    def deplacement(self):
        pass




################ Spatial ############################## 

    def deplacement_acteur(self,new_x,new_y):
        self.x = new_x
        self.y = new_y
        self.rect.topleft = (720 + taillecase *self.x,taillecase *self.y)





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
        self.x = round(nouvelle_pos.x)
        self.y = round(nouvelle_pos.y)

        ## Synchronisation avec le visuel 
        self.rect.topleft = (720 + taillecase *self.x,taillecase *self.y)
        self.rect_img.center = self.rect.center


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





    


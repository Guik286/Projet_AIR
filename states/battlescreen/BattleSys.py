import pygame
from settings import *
from states.acteurs.acteur import Acteur
import random as rd

class control_joueur:
    def __init__(self,player):
        self.player = player #chargement du joueur
        self.player.etat_jeu = "menu" ## Par défaut
        self.menuBattScreen = self.player.menuBattScreen #Menu du joueur
        self.Attaque = self.player.Attaque # ensemble d'atq joueur
        self.Attaque_index = self.player.Attaque_index #Index de l'atq select dans le roster
        self.Index_cible = 0 # Permet de selectionner la cible en mode map
        self.damage = 0 ## Dommages d'une attaque
        






    def input_menu(self,event,index,options):
        if index > len(options):
            index = 0


        if event.type == pygame.KEYDOWN:
        
            if event.key == pygame.K_UP:
                if index <=0:
                    index = len(options)-1
                else:
                    index -= 1
            elif event.key == pygame.K_DOWN:
                if index >= len(options)-1:
                    index = 0
                else:
                    index +=1
            return index
        
    def pointage_map(self):
        pass
        
        



    def logique_echap(self,player,acteur):

            if player.etat_jeu == "cible":
                player.etat_jeu = "attaque"


            elif player.etat_jeu in ["attaque","map"]:
                player.etat_jeu = "menu"
                player.wait = False
                for i in range(0,len(acteur),1):
                    acteur[i].wait = False
            




    def logique_valider(self,event,player,cible,cout_total,index_menu,acteurs,index):
        if event.key == pygame.K_RETURN:

            #Commande menu
            if player.etat_jeu == "menu" and player.etat == "jouable":
                self.player.wait = True
        
                player.etat_jeu = player.menuBattScreen[(index_menu+1)]
                for i in range(0,len(acteurs),1):
                    acteurs[i].wait = True
            ##Commande attaque
            elif player.etat_jeu == "attaque":
                

                ## on selectionne une attaque

                player.etat_jeu = "cible"
                
                ### prévoir un Attaque_index de plus pour avoir une valeur pour reset le menu attaque
        
            ### Commande Cible
            ### Quand on a selectionné une attaque, on selectionne une cible
            elif player.etat_jeu == "cible":

                ## Flag PA :
                if not logique_de_combat(player,cible,index).flag_PA:
                    
                    logique_de_combat(player,cible,index).exec_atq()

                    player.chrono_action = 5*player.dureetour/6 + 0.1 # On set le point de départ du chrono de l'attaque (zone de cast a definir en init)
                    for i in range(0,len(acteurs),1):
                        acteurs[i].wait = False
                    player.wait = False
                    player.etat_jeu = "menu"
                    player.etat = "casting"
                    player.etat_jeu = "menu"                                  
                    player.Attaque_index = 0
                else:
                    print("Pas assez de PA")
                    pass
                    

                
            elif player.etat_jeu == "map":
                # Vérifie si le joueur a assez de PA
                if player.PA >= cout_total:
                    # Effectue le déplacement
                    player.rect.x = player.curseur.x
                    player.rect.y = player.curseur.y
                    # Dépense les PA
                    player.PA -= cout_total
                    # Reset l'état
                    player.chrono_action = 5 * player.dureetour / 6 + 0.1
                    player.etat = "casting"
                    player.etat_jeu = "menu"
                    player.wait = False
                    for i in [0]:
                        acteurs[i].wait = False
                    
    
class logique_de_combat:
    def __init__(self,striker,target,index):
        self.striker = striker
        self.cible = target
        self.flag_PA = True
        self.index = index


        self.skill_set = striker.Attaque
        
        ##On check les points d'actions en invoquant la classe
        self.Check_PA()


    def Check_PA(self):
        if self.striker.PA < self.skill_set.stat[self.skill_set.names[self.index]]['PA']:
            self.flag_PA = True
            print("Not Enough PA !")
        else:
            self.flag_PA = False

    #def knockback(self):
#
    #    # Position de l'attaquant
    #    pos_attaquant = pygame.math.Vector2(self.striker.rect.center)
    #    # Position de la cible
    #    pos_cible = pygame.math.Vector2(self.cible.rect.center)
#
    #    # Calcul du vecteur de knockback (direction de la poussée)
    #    direction = pos_cible - pos_attaquant
#
#
    #    if direction.length() != 0:  # Évite la division par zéro
    #        direction = direction.normalize()
#
    #    knockback_distance = self.skill_set.stat[self.skill_set.names[self.index]]['KB']*60
    #    nouvelle_pos = pos_cible + direction * knockback_distance
    #        
    #    # Appliquer le déplacement visuel
    #    self.cible.rect.centerx = int(nouvelle_pos.x)
    #    self.cible.rect.centery = int(nouvelle_pos.y)
#
#
    #    # --- Synchroniser la position logique (si présente) ---
    #    # Exemple : si l'acteur garde des coordonnées de case (case_x, case_y)
    #    if hasattr(self.cible, "case_x") and hasattr(self.cible, "case_y"):
    #        # convertir pixels -> indices de case (ajuster offset / taille si différent)
    #        self.cible.case_x = int((self.cible.rect.x - 720) // taillecase)
    #        self.cible.case_y = int(self.cible.rect.y // taillecase)
    #    # Exemple : attribut générique grid_pos = (x,y)
    #    elif hasattr(self.cible, "grid_pos"):
    #        print(hasattr(self.cible, "grid_pos"))
    #        gx = int((self.cible.rect.x - 720) // taillecase)
    #        gy = int(self.cible.rect.y // taillecase)
    #        self.cible.grid_pos = (gx, gy)
    #        print(gx,gy)
    #    # Sinon, stocker la nouvelle position comme position source pour éviter override
    #    else:
    #        self.cible.base_pos = (self.cible.rect.x, self.cible.rect.y)
#
#
#
#
    #        # Animation optionnelle de recul (à implémenter si souhaité)
    #    self.cible.hit = True  # Flag pour indiquer que l'acteur a été touchés
    #        #def flash_on_hit(self,acteur):
    #        #    if acteur.hit == True:
       

    def calcul_dommage(self):
        self.damage = self.striker.force*2 + self.skill_set.stat[self.skill_set.names[self.index]]['FOR'] - self.cible.defense
        return self.damage



    def exec_atq(self):
        ### nom de l'attaque
        self.name = self.skill_set.names[self.index]
        ## check si activable

        self.cible.lp -= max(0,self.calcul_dommage())
        self.cible.hit = True
        self.cible.get_striked(self.striker,self.skill_set.stat[self.skill_set.names[self.index]])

        ## On vérifie si on a la portée










    

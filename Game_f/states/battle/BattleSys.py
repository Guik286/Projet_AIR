import pygame
from settings import *
from Game_f.states.acteurs.acteur import Acteur
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



    def calcul_dommage(self):
        self.cible.defense = max(1,self.cible.defense ) ## Pour éviter la division par 0
        base = self.skill_set.stat[self.skill_set.names[self.index]]['FOR']
        self.cible.damage = base * (1+self.striker.force/self.cible.defense) * rd.uniform(0.85,1.15)
        self.cible.damage = int(self.cible.damage)

        



    def exec_atq(self):
        ### nom de l'attaque
        self.name = self.skill_set.names[self.index]
        self.calcul_dommage()
        ## check si activable

        self.cible.lp -= max(0,self.cible.damage)
        print(self.cible.lp)
        self.cible.hit = True
        self.cible.get_striked(self.striker,self.skill_set.stat[self.skill_set.names[self.index]])

        ## On vérifie si on a la portée










    

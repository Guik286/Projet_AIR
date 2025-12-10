import pygame
from Game_f.states.base import BaseState
from Game_f.states.acteurs.acteur import Acteur
from Game_f.states.acteurs.Joueur.joueur import Joueur
from Game_f.states.acteurs.ennemi import Ennemi
from GI import GraphicInterface

import random as rd


from Data.settings import *
from Game_f.states.battle.ATB import *
from .BattleSys import control_joueur, logique_de_combat
from .battlelogic import Matrice_Bagarre




#### EN SUSPENS : faire un autre etat pour le joueur "map" "menu" "jeu" et changer les flags correspondant. 


class Level(BaseState):
    def __init__(self):
        super(Level, self).__init__()
        self.time_active = 0
        self.time = pygame.time.Clock()

        self.BL = logique_de_combat
        

        ### Parametres de temps

        self.time_anim = 0


        
        self.active_index = 0

        self.grid = [[None] * ncol for j in range(nrow) ]

        
        

        
        ## commande menu activées, désactivées

        #### Tout les rectangles

        ## Les sprites

        #self.player = Joueur(720+taillecase*self.x,taillecase*self.y)
        #720+ taillecase *rd.randint(0,5),taillecase *rd.randint(0,5)
        self.player = Joueur()
        self.ennemi = Ennemi(rd.randint(15,nrow-1),rd.randint(14,ncol-1))
        self.control = control_joueur(self.player)

        self.ennemi2 = Ennemi(rd.randint(15,nrow-1),rd.randint(14,ncol-1))

        self.ref = Acteur(0,0)
        self.Ennemis = [self.ennemi,self.ennemi2]
        for ennemi in self.Ennemis:
            print(ennemi.x,ennemi.y)
            
        
        self.Index_cible = 0

        self.couleur_E = [pygame.Color("purple"),pygame.Color("cyan"),pygame.Color("darkred")]
        
        ## Cout des actions 
        self.cout_deplacement = 300 ## PlayTEST
        ### Test import Json
        self.texte_attaque = self.player.Attaque.names



        ## Image 
        self.font_dmg = pygame.font.SysFont("Arial",50)
        self.position_grille()
        
        

    

    def position_grille(self):
        self.grid[self.player.x][self.player.y] = self.player
        
        for ennemi in self.Ennemis:
            self.grid[ennemi.x][ennemi.y] = ennemi
                # self.grid[i][j] = Objet_BS[self.grid[i][j]]

    
    def grid_to_arena(self):
        index = 0
        for i in range(0,nrow,1):
            for j in range(0,ncol,1):

                if self.grid[i][j] == "Joueur":
                    self.player.x, self.player.y = i,j 
                elif self.grid[i][j] == "Ennemi":
                    self.Ennemis[index].x,self.Ennemis[index].y = i,j
                    index += 1
                else:
                    pass
    def deplacer_grid(self,old_x,old_y,acteur):
        
        x_new,y_new = acteur.x,acteur.y
        self.grid[x_new][y_new] = self.grid[old_x][old_y]
        self.grid[old_x][old_y] = None
        

            

    

#### Conditions de sortie vers Fin
    def Defaite(self):
        if self.player.etat == "mort":
            self.next_state = "GAME_OVER"
            self.done = True

    def Fin_Joueur(self):
        self.player.mort()
        self.Defaite()

#### fin adversaire

    def Ennemi_out(self):
        for i in range(0,len(self.Ennemis),1):

            if self.Ennemis[i].lp <= 0:
                self.Ennemis[i].mort()
                self.Ennemis.pop(i)
                self.couleur_E.pop(i+1)
                self.Index_cible = 0
                
                break

### Conditions de sortie vers suite


    def Victoire(self):

            if self.Ennemis == []:
                self.next_state = "Victoire"
                self.done = True
                self.player.experience += 1



################################################################## UPDATE ###############################################################
################################################## APPEL DANS GAME ######################################################################
    ### Calcul du temps
    def update(self, dt):

        
        ## Calcul temps ref
        self.ref.calcul_temps_ref(dt)

        ### Horloge joueur
        self.player.calcul_temps_acteur(self.ref.dureetour,dt)

        # Horloge adversaires
        for i in range(0,len(self.Ennemis),1):
            self.Ennemis[i].calcul_temps_acteur(self.ref.dureetour,dt)


        ### déclenche IA adversaires f(horloge)
        for i in range(0,len(self.Ennemis),1):
            limite = rd.randint(3,5)

            

            if self.Ennemis[i].etat == "jouable":
                
                
                if self.Ennemis[i].chrono_action <= limite:
                    self.Ennemis[i].Calcul_PA()
                    
                else:
                    old_x = self.Ennemis[i].x
                    old_y = self.Ennemis[i].y
                    self.Ennemis[i].IA_ennemi(self.player,self.grid)
                    self.deplacer_grid(old_x,old_y,self.Ennemis[i])
                    #print(self.grid)
            self.Ennemis[i].ordonnee_indicateur()

        ### Sortie vers Fin
        self.Fin_Joueur()
        #### Fin ennemis
        self.Ennemi_out()
        ### Sortie vers suite.
        self.Victoire()


        
    ################################################################## GRAPHIQUES #################################################################

    ###############################################################################################################################################



################################################## ANIMATION ###################################################
    def Animation_attaque(self):
        ## Variable : Acteur effectuant l'attaque, attaque choisie 
        ## On charge l'attaque sélectionnés à partir d'un dico
        ## on execute un temps de "cast"
        ## animation de l'attaque et calcul des dégats (self.Stop_time_active à enclencher pendant cette phase)
        pass

    def Animation_déplacement(self):
        ## Variable : Acteur effectuant le déplacement
        # On effectue le déplacements de l'entité sur la carte 
        pass

    #Formattage du texte des menus

#### text des divers menus et leurs positionnements


#### Affiche les dommages 
    def display_dmg(self,dommage):
        self.phrase_dmg = self.font_dmg.render(f"{dommage}",True,(0,0,0))
        return self.phrase_dmg
    
###### Selection de l'ennemi 
    def selection_ennemi(self,index):
        color = pygame.Color("red") if index == self.Index_cible else pygame.Color("white")
        return color
    
    


######################## AFFICHAGE : Appelé dans GAME ###################################


    def draw(self,surface):

        ## Fond de l'écran

        ### Background
        surface.fill(pygame.Color('black'))

        ## Arene 

        

        pygame.draw.rect(surface,pygame.Color("white"), Batt_Area)
        surface.blit(Image_A,(720,0))
        ### Menu joueur
        pygame.draw.rect(surface,pygame.Color("lightblue"), Commande_Joueur)
        #Echiquier (tracer de ligne)


        for i in range(720,1920,taillecase):
            for j in range(0,1080,taillecase):
                rect = pygame.Rect((i,j),(taillecase,taillecase))
                pygame.draw.rect(surface,"black",rect,1)

        
        
        #Barre de temps
        for i in Battle_screen:
            i.draw_ATB(surface)
        ### Vitesse des acteurs et acteurs
        
        ### Affichage des adversaires

        if self.Ennemis != []:
            for i in range(0,len(self.Ennemis),1):
                pygame.draw.rect(surface,self.couleur_E[(i+1)],self.Ennemis[i].rect_indicateur)
                pygame.draw.rect(surface,self.couleur_E[(i+1)],self.Ennemis[i].rect)


                surface.blit(self.Ennemis[i].image,self.Ennemis[i].rect_img)
                self.Ennemis[i].hit -= 1 
                if self.Ennemis[i].hit < 1 :
                    self.Ennemis[i].image_hit()
                
            #
                #if self.Ennemis[i].hit == True:
                #    if pygame.time.get_ticks() - self.starttime <= 200:
                #        surface.blit(self.display_dmg(self.BL(self.player,self.Ennemis[i],self.player.Attaque_index).calcul_dommage()),(self.Ennemis[i].rect.center)+(300,300))
                #    else:
                #        surface.blit(self.display_dmg(self.BL(self.player,self.Ennemis[i],self.player.Attaque_index).calcul_dommage()),(self.Ennemis[i].rect.center))
                #    if pygame.time.get_ticks() - self.starttime >= 300:
                #        self.Ennemis[i].hit = False
#

        #### Affichage du/des joueurs

        self.player.ordonnee_indicateur()
        pygame.draw.rect(surface,self.couleur_E[0],self.player.rect_indicateur)
        pygame.draw.rect(surface, self.couleur_E[0], self.player.rect)
        self.ref.ordonnee_indicateur()
        pygame.draw.rect(surface,pygame.Color("black"),self.ref.rect_indicateur) 
        


        ## Affichage ou non du Menu d'attaque
        
        if self.player.etat_jeu == "attaque" or self.player.etat_jeu == "cible":
            pygame.draw.rect(surface, pygame.Color("blue"), Objet_attaque)

            GraphicInterface(self.texte_attaque,self.player.Attaque_index,Objet_attaque).draw(surface)
        if self.player.etat_jeu == "cible":
            for index, ennemi in enumerate(self.Ennemis):
                pygame.draw.rect(surface,self.selection_ennemi(self.Index_cible),self.Ennemis[self.Index_cible].rect,3)


        ### Affichage des options du menu
        GraphicInterface(Option_BS,self.active_index,Commande_Joueur).draw(surface)

        
        ## Affichage des déplacements possibles
        if self.player.etat_jeu == "map":
            self.player.afficher_deplacement_possible(surface,self.grid)
            pygame.draw.rect(surface,pygame.Color("yellow"),self.player.curseur,3)

        if self.player.etat == "casting":
            pass
        ##Declenche une animation

        
############################################ DETECTION DES EVENTS (COMMANDES) ########################################################
######################################################################################################################################

    def get_event(self,event):


        player_x, player_y = (self.player.rect.x - 720) // taillecase, self.player.rect.y // taillecase

        self.player.PA = round(2 * self.player.chrono_action*1000 / self.player.dureetour)
        
        max_cases = self.player.PA // self.player.cout_deplacement
        # Position actuelle en coordonnées de grille
        current_x,current_y = (self.player.curseur.x - 720) // taillecase,self.player.curseur.y // taillecase

        distance = abs(current_x - player_x) + abs(current_y - player_y)
        cout_total = distance * self.player.cout_deplacement


        if event.type == pygame.QUIT:
            self.quit = True
        

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit = True

            elif event.key == pygame.K_RETURN:
                
                
                self.control.logique_valider(event,self.player,self.Ennemis[self.Index_cible],cout_total,self.active_index,self.Ennemis,self.player.Attaque_index)
                self.starttime = pygame.time.get_ticks()
                
        ## On repart en arriere
            elif event.key == pygame.K_BACKSPACE:
                self.control.logique_echap(self.player,self.Ennemis)

            elif event.key in [pygame.K_UP,pygame.K_DOWN]:
                if self.player.etat_jeu == "menu":

                    self.active_index = self.control.input_menu(event,self.active_index,Option_BS)
                elif self.player.etat_jeu == "attaque":

                    self.player.Attaque_index = self.control.input_menu(event,self.player.Attaque_index,self.texte_attaque)
                elif self.player.etat_jeu == "cible":

                    self.Index_cible = self.control.input_menu(event,self.Index_cible,self.Ennemis)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.player.etat_jeu == "map":
                ## Position logique
                ### Position du joueur
                pos_i = self.player.x
                pos_j = self.player.y
                ## On récupère la position du clic de la souris
                pos = pygame.math.Vector2(pygame.mouse.get_pos())
                #detecter la case cliquée
                col = int((pos.x - 720) // taillecase)
                row = int(pos.y // taillecase)
                #print(row,col)
                #print(self.grid)
                ## Quand il y'aura un algo de pathfinding, on l'appellera ici
                ## On permute les valeurs dans la matrice
                self.grid[pos_i][pos_j] = None
                self.grid[row][col] = self.player
                self.player.deplacement_acteur(col,row)
                ## On met à jour les coordonnées du joueur  
                
                ## On déplace le sprite du joueur
                
                

                

                

                #pos_J = pygame.math.Vector2(self.player.rect.center)
                #
                #self.player.x,self.player.y = pos
                #print(self.player.x,self.player.y)
                #movement = pos - pos_J
                #self.player.rect.move_ip(movement)
                #self.player
                self.player.chrono_action = 0
                self.player.etat = "cooldown"
                self.player.etat_jeu = "menu"
                self.player.wait = False
                for i in range(0,len(self.Ennemis),1):
                    self.Ennemis[i].wait = False






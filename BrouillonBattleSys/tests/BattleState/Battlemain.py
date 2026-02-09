import pygame
from BrouillonBattleSys.tests.BattleState.Entites.EntitesLogique.Point2D import Point2D
from BrouillonBattleSys.tests.BattleState.Entites.EntitesLogique.Objet2D import objet2D, Acteur

from BrouillonBattleSys.tests.BattleState.Map.MapLogique.MatriceLogique import GrilleCombat
from settingsBrouillonBS import *
from random import randint as rd



from BattleSysteme import EffetSpatiaux, GraphObjet as GO, Gestion_Acteur as GA, RegleCombat as RC

class Battle:
    def __init__(self):

        # Objectif : Encapsuler tous les init dans un système de sauvegarde

        ## Controle du joueur
        

        ### Charger Map 

        ### Ici la map logique ##########################
        ## Hérité de classe
        self.grillelogique = GrilleCombat(ncol,nrow)
        ### Systeme de combat 

        self.DeplaLogique = EffetSpatiaux(self.grillelogique)
        self.JoueurLogique = Acteur(9,10,"Joueur","Un Joueur fort et courageux!",100,15,"no_alt",None,5,1, 100)
        
        self.grillelogique.placer_element(self.JoueurLogique)
        self.Relation = GA(self.JoueurLogique,self.grillelogique)

        

        ### Graphisme : 

        

        ### Objets logiques ########################


        self.Murs = []
        self.MursRect = []
        ### Pour petit test
        #x, y = [0,1,2,3,4],[4,4,4,4,4]
        #for i in range(0,5,1):
        #    
        #    self.Murs.append(Point2D(x[i],y[i],f'Mur{i}'))
        #    self.MursRect.append(pygame.Rect(self.Murs[i].x*taillecol,self.Murs[i].y*taillerow,taillecol,taillerow))
        #w, z = [4,4],[5,6]
        #for i in range(0,2,1):
        #    
        #    self.Murs.append(Point2D(w[i],z[i],f'Mur{5+i}'))
        #    self.MursRect.append(pygame.Rect(self.Murs[5+i].x*taillecol,self.Murs[5+i].y*taillerow,taillecol,taillerow))
        #### Pour les gros test
        for i in range(4):
            x,y = rd(1,8),rd(1,8)
            self.Murs.append(objet2D(x,y,f'Mur{i}','Un mur infranchissable',lp_max=10,defense=1,Image=None))
            self.MursRect.append(pygame.Rect(self.Murs[i].x*taillecol,self.Murs[i].y*taillerow,taillecol,taillerow))

        
        for mur in self.Murs:
            self.grillelogique.placer_element(mur)


        ######### Acteurs logiques ##################
        self.EnnemiLogique = Acteur(0,0,"Ennemi","Un Ennemi",10,1,"no_alt",None,2,10)
        self.grillelogique.placer_element(self.EnnemiLogique)





        #### Graphisme
        
        
        self.grillegraphique = pygame.Rect((0,0),(length,height))

        self.taillecase = (taillecol,taillerow)
        print(f'longueur: {length},hauteur: {height},nlignes: {nrow},ncolonnes: {ncol},taillecase: {self.taillecase}')



        self.JoueurRectangle = GO(self.JoueurLogique).rectangle
        pygame.Rect(self.JoueurLogique.x * taillecol, self.JoueurLogique.y * taillerow, taillecol, taillerow)

        self.IndMovePlayer = False
        self.xclick = 0
        self.yclick = 0
        

        
        self.EnnemiRectangle = GO(self.EnnemiLogique).rectangle


        ##### Horloge 

        self.temps = 0
        self.screen = pygame.Surface((1000, 800))

        ## Animation (le chemin joueur ne parviens pas à la derniere case)
        self.AnimStop = 0
        
        ## Pathfinding
        self.k = 1
        self.indicateur_path = False


        print(f"Les points de vie de l'ennemi sont:{self.EnnemiLogique.lp}")

        print("Initialisation du système de contrôle")
        print(f"Liste initiative : {RC([self.JoueurLogique,self.EnnemiLogique]).tirer_initiative()}")


        



        

        



    #### Partie point




    ## Principalement les controles du joueur ##
    def get_event(self, event):
        if self.controle.is_new_key_press("start") == True:
            self.path = []
            self.k = 0
            self.path = self.grillelogique.pathfinding(self.JoueurLogique,self.EnnemiLogique)
            if self.path is None:
                print("Pas de chemin trouvé vers l'ennemi.")
                self.indicateur_path = False
            self.pathRect = []
            if len(self.path) == 2:
                print("L'ennemi est juste à coté")
                self.indicateur_path = False
            for point in self.path:
                self.pathRect.append(pygame.Rect(point.x * taillecol, point.y * taillerow, taillecol, taillerow))
            if len(self.path) > 2:
                self.indicateur_path = True

        elif self.controle.is_new_key_press("select"):
            self.pause_joueur = True
            if self.grillelogique.grid[9][9].element != self.EnnemiLogique:

                self.grillelogique.deplacer_element(self.EnnemiLogique,9,9)
                self.EnnemiRectangle = GO(self.EnnemiLogique).rectangle
                
            else:
                pass

        elif self.controle.is_new_key_press("A"):
            GA(self.JoueurLogique,self.grillelogique).attaque(self.EnnemiLogique)
            self.EnnemiRectangle = GO(self.EnnemiLogique).rectangle
        elif event.type == pygame.MOUSEBUTTONDOWN:
                self.grillelogique.print_element(self.JoueurLogique.x,self.JoueurLogique.y)
                self.path = []
                self.k = 0
                pos = pygame.math.Vector2(pygame.mouse.get_pos())
                self.xclick = int(pos.x//taillecol)
                self.yclick = int(pos.y//taillerow)

                ## On récupère la position du clic de la souris
                
                self.path = self.grillelogique.pathfinding(self.grillelogique.grid[self.xclick][self.yclick],self.JoueurLogique)
                self.limite = self.DeplaLogique.reduction_chemin(self.JoueurLogique) + 1


                if len(self.path) <= 1:
                    print("Sur place.")
                    self.IndMovePlayer = False
                else:
                    self.IndMovePlayer = True
                #self.DeplaLogique.Mouvement(self.JoueurLogique,self.k,path)
                #self.grillelogique.deplacer_element(self.JoueurLogique,newx,newy)
                #self.JoueurRectangle = GO(self.JoueurLogique).rectangle
        elif self.controle.is_new_key_press("B"):
            self.EnnemiLogique.lp -=1
            self.EnnemiLogique.mort()
            print(f"Lp ennemi restant : {self.EnnemiLogique.lp}")
            if self.EnnemiLogique.Etat == "mort":
                self.grillelogique.retirer_element(self.EnnemiLogique.x,self.EnnemiLogique.y)
                self.grillelogique.print_element(self.EnnemiLogique.x,self.EnnemiLogique.y)
            
        

                    




    



    ### Horloge, fournira l'ATB et autres systemes temporels ###
    def horloge(self, dt):
        self.temps += dt

        ## Generer des PA pour le joueur
        self.JoueurLogique.Barre_action(dt)
        self.JoueurLogique.Barre_resolution(dt)
        self.JoueurLogique.generer_PA()

        #Ennemi
        self.EnnemiLogique.Barre_action(dt)
        self.EnnemiLogique.Barre_resolution(dt)
        


        ### Comportement ennemi simple : deplace vers le joueur des qu'il a assez de PA pour faire une action
        self.EnnemiLogique.IA_Ennemi(dt,self.grillelogique,self.DeplaLogique,self.JoueurLogique)

        self.EnnemiRectangle = GO(self.EnnemiLogique).rectangle
        
        if self.indicateur_path == True:
            #self.grillelogique.afficher_grille()
            self.k += 1 
            self.DeplaLogique.Mouvement(self.EnnemiLogique,self.k,self.path)
            #self.EnnemiRectangle = GO(self.EnnemiLogique).rectangle

            if len(self.path) - self.k == 1:
                self.indicateur_path = False
                
        if self.IndMovePlayer == True:
            if self.k + 1 <= self.limite:
                self.k += 1
                print(f"Déplacement numéro {self.k} du joueur.")
                if self.grillelogique.grid[self.xclick][self.yclick].element == self.EnnemiLogique:
                    self.JoueurLogique.get_voisins(self.grillelogique)
                    if self.grillelogique.grid[self.xclick][self.yclick] in self.JoueurLogique.voisins:
                        print("Attaque possible !")
                        GA(self.JoueurLogique,self.grillelogique).attaque(self.EnnemiLogique)
                        self.EnnemiRectangle = GO(self.EnnemiLogique).rectangle
                        self.IndMovePlayer = False
                        return
                self.DeplaLogique.Mouvement(self.JoueurLogique,self.k,self.path)
                self.JoueurRectangle = GO(self.JoueurLogique).rectangle
            else:
                self.IndMovePlayer = False



                

                
                
                #On creer un repère dans le temps pour eviter les deplacements instantanés

                 # 500 ms de delai entre chaque deplacement

    
    


    ##### Partie graphique, elle appellera la partie logique #####
    ### Penser à caler la partie logique sur X fps, mais l'affichage a X/3 fps ###
    def draw(self, surface):
        surface.fill((255, 255, 255))
        font = pygame.font.Font(None, 30)
        text = font.render(f'Temps: {int(self.temps)}s', True, (0, 0, 0)) # 1.38 empirique deviation quelques centiemes de secondes après 20 secondes
        pygame.draw.rect(surface,pygame.Color("White"),self.grillegraphique)

        ## Grille
        for x in range(0, length, taillecol):
            for y in range(0, height, taillerow):
                rect = pygame.Rect((x, y), (taillecol, taillerow))
                pygame.draw.rect(surface, "Black", rect, 1)

        GO(self.JoueurLogique).Dessiner_Objet(surface)

        if self.EnnemiLogique.Etat != "mort":
            GO(self.EnnemiLogique).Dessiner_Objet(surface)

        for rect in self.MursRect:
            pygame.draw.rect(surface,"brown",rect)

        if self.indicateur_path == True:
            for point in self.pathRect:
                pygame.draw.rect(surface,"green",point)
                GO(self.EnnemiLogique).Dessiner_Objet(surface)
                GO(self.JoueurLogique).Dessiner_Objet(surface)
                #pygame.draw.rect(surface,"yellow",self.EnnemiRectangle)


        
        surface.blit(text, (0,0))
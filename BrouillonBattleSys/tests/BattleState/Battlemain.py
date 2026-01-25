import pygame
from BrouillonBattleSys.tests.BattleState.Entites.EntitesLogique.Point2D import Point2D
from BrouillonBattleSys.tests.BattleState.Map.MapLogique.MatriceLogique import GrilleCombat
from settingsBrouillonBS import *
from random import randint as rd

from KeysManager import KeysManager

class Battle:
    def __init__(self):

        # Objectif : Encapsuler tous les init dans un système de sauvegarde

        ## Controle du joueur
        self.controle = KeysManager()
        

        ### Charger Map 

        ### Ici la map logique ##########################

        self.grillelogique = GrilleCombat(nrow,ncol)

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
            self.Murs.append(Point2D(x,y,f'Mur{i}'))
            self.MursRect.append(pygame.Rect(self.Murs[i].x*taillecol,self.Murs[i].y*taillerow,taillecol,taillerow))

        
        for mur in self.Murs:
            self.grillelogique.placer_element(mur)


        ######### Acteurs logiques ##################
        self.EnnemiLogique = Point2D(9,9,"Ennemi")
        self.grillelogique.placer_element(self.EnnemiLogique)

        self.JoueurLogique = Point2D(0,0,"Joueur")
        self.grillelogique.placer_element(self.JoueurLogique)

        #### Graphisme
        
        
        self.grillegraphique = pygame.Rect((0,0),(length,height))

        self.taillecase = (taillecol,taillerow)
        print(f'longueur: {length},hauteur: {height},nlignes: {nrow},ncolonnes: {ncol},taillecase: {self.taillecase}')



        self.JoueurRectangle = pygame.Rect(self.JoueurLogique.x * taillecol, self.JoueurLogique.y * taillerow, taillecol, taillerow)
        

        
        self.EnnemiRectangle = pygame.Rect(self.EnnemiLogique.x * taillecol, self.EnnemiLogique.y * taillerow, taillecol, taillerow)
        

        ##### Horloge 

        self.temps = 0
        self.screen = pygame.Surface((1000, 800))
        self.k = 1


        self.indicateur_path = False
        self.grillelogique.print_element(1,1)
        



        

        



    #### Partie point




    ## Principalement les controles du joueur ##
    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif self.controle.is_key_down("start"):
                
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
                if len(self.path) != 2:
                    self.indicateur_path = True
                self.controle.input = False

                    




    



    ### Horloge, fournira l'ATB et autres systemes temporels ###
    def horloge(self, dt):
        self.temps += dt
        self.grillelogique.print_element(1,1)
        if self.indicateur_path == True:
            #self.grillelogique.afficher_grille()
            self.k += 1 
            longueur_chemin = len(self.path)
            case_actuelle = self.path[longueur_chemin -min(self.k,longueur_chemin)]
            x = case_actuelle.x
            y = case_actuelle.y
            print(f"le temps self.temps est :{self.temps}")
            try:
                self.grillelogique.deplacer_element(self.EnnemiLogique, x, y)
                print(f"L'indice d'évolution sur le chemin est :{self.k}")
                
            except ValueError as e:
                print(f"Déplacement impossible vers ({x},{y}) : {e}")
                print(f"L'indice d'évolution sur le chemin est :{self.k}")
            print("élément en 1,1")
            self.grillelogique.print_element(1,1)
            print("élément en 9,9")
            self.grillelogique.print_element(9,9)
           

            # Debug: afficher état du chemin et de la grille après déplacement
            #try:
            #    chemin_info = [(p.x, p.y, 'occ' if p.element else 'free') for p in self.path]
            #    print("Chemin (x,y,etat):", chemin_info)
            #except Exception as e:
            #    print("Erreur affichage chemin:", e)
#
            #try:
            #    print("Grille:")
            #    self.grillelogique.afficher_grille()
            #except Exception as e:
            #    print("Erreur affichage grille:", e)
#
            #try:
            #    self.grillelogique.draw_path(self.path)
            #except Exception as e:
            #    print("Erreur draw_path:", e)

            self.EnnemiRectangle = pygame.Rect(self.EnnemiLogique.x * taillecol, self.EnnemiLogique.y * taillerow, taillecol, taillerow)
            if longueur_chemin - self.k == 1:
                self.indicateur_path = False
    
    


    ##### Partie graphique, elle appellera la partie logique #####
    ### Penser à caler la partie logique sur X fps, mais l'affichage a X/3 fps ###
    def draw(self, surface):
        surface.fill((255, 255, 255))
        font = pygame.font.Font(None, 30)
        text = font.render(f'Temps: {int(self.temps/1000)}s', True, (0, 0, 0))
        pygame.draw.rect(surface,pygame.Color("White"),self.grillegraphique)

        ## Grille
        for x in range(0, length, taillecol):
            for y in range(0, height, taillerow):
                rect = pygame.Rect((x, y), (taillecol, taillerow))
                pygame.draw.rect(surface, "Black", rect, 1)
        pygame.draw.rect(surface,"purple",self.JoueurRectangle)
        pygame.draw.rect(surface,"yellow",self.EnnemiRectangle)
        for rect in self.MursRect:
            pygame.draw.rect(surface,"brown",rect)
        if self.indicateur_path == True:
            for point in self.pathRect:
                pygame.draw.rect(surface,"green",point)
                pygame.draw.rect(surface,"purple",self.JoueurRectangle)
                pygame.draw.rect(surface,"yellow",self.EnnemiRectangle)


        
        surface.blit(text, (0,0))
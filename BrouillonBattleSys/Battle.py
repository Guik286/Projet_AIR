import pygame
from BrouillonBattleSys.Pointetmatricelogique.EssaiPoint2D import Point2D, objet2D
from BrouillonBattleSys.Pointetmatricelogique.EssaiMatriceLogique import GrilleCombat
from BrouillonBattleSys.settingsBrouillonBS import *
from random import randint as rd

class Battle:
    def __init__(self):
        self.temps = 0
        self.screen = pygame.Surface((1000, 800))
        self.k = 1

        self.grillelogique = GrilleCombat(nrow,ncol)
        
        self.grillegraphique = pygame.Rect((0,0),(length,height))

        self.taillecase = (taillecol,taillerow)
        print(f'longueur: {length},hauteur: {height},nlignes: {nrow},ncolonnes: {ncol},taillecase: {self.taillecase}')




        self.JoueurLogique = Point2D(0,0,"Joueur")
        self.JoueurRectangle = pygame.Rect(self.JoueurLogique.x,self.JoueurLogique.y,taillerow,taillecol)
        self.grillelogique.placer_element(self.JoueurLogique)

        self.EnnemiLogique = Point2D(49,49)
        self.EnnemiRectangle = pygame.Rect(self.EnnemiLogique.x*taillerow,self.EnnemiLogique.y*taillecol,taillerow,taillecol)
        self.grillelogique.placer_element(self.EnnemiLogique)

        self.Murs = []
        self.MursRect = []
        ### Pour petit test
        #x, y = [0,1,2,3,4],[4,4,4,4,4]
        #for i in range(0,5,1):
        #    
        #    self.Murs.append(Point2D(x[i],y[i],f'Mur{i}'))
        #    self.MursRect.append(pygame.Rect(self.Murs[i].x*taillerow,self.Murs[i].y*taillecol,taillerow,taillecol))
        #w, z = [4,4],[5,6]
        #for i in range(0,2,1):
        #    
        #    self.Murs.append(Point2D(w[i],z[i],f'Mur{5+i}'))
        #    self.MursRect.append(pygame.Rect(self.Murs[5+i].x*taillerow,self.Murs[5+i].y*taillecol,taillerow,taillecol))
        #### Pour les gros test
        for i in range(1500):
            x,y = rd(1,48),rd(1,48)
            self.Murs.append(Point2D(x,y,f'Mur{i}'))
            self.MursRect.append(pygame.Rect(self.Murs[i].x*taillerow,self.Murs[i].y*taillecol,taillerow,taillecol))

        
        for mur in self.Murs:
            self.grillelogique.placer_element(mur)

        self.indicateur_path = False
        self.grillelogique.afficher_grille()


        

        



    #### Partie point




    ## Principalement les controles du joueur ##
    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_SPACE:
                self.indicateur_path = True
                self.path = self.grillelogique.pathfinding(self.JoueurLogique,self.EnnemiLogique)
                if self.path is None:
                    print("Pas de chemin trouvé vers l'ennemi.")
                    self.indicateur_path = False
                    return
                self.nomchemin = []
                self.pathRect = []
                for point in self.path:
                    self.pathRect.append(pygame.Rect(point.x*taillerow,point.y*taillecol,taillerow,taillecol))
                    

                    if point.element is None:
                        self.nomchemin.append(point.nom)
                    else:
                        self.nomchemin.append(point.element.nom)
                print(self.nomchemin)


    



    ### Horloge, fournira l'ATB et autres systemes temporels ###
    def horloge(self, dt):
        self.temps += dt
        if self.indicateur_path == True:
            #self.grillelogique.afficher_grille()
            self.k += int(self.temps) 
            longueur_chemin = len(self.path)
            case_actuelle = self.path[longueur_chemin -min(self.k,longueur_chemin)]
            print(case_actuelle.x,case_actuelle.y)
            x = case_actuelle.x
            y = case_actuelle.y
            try:
                self.grillelogique.deplacer_element(self.EnnemiLogique, x, y)
            except ValueError as e:
                print(f"Déplacement impossible vers ({x},{y}) : {e}")
           

            # Debug: afficher état du chemin et de la grille après déplacement
            try:
                chemin_info = [(p.x, p.y, 'occ' if p.element else 'free') for p in self.path]
                print("Chemin (x,y,etat):", chemin_info)
            except Exception as e:
                print("Erreur affichage chemin:", e)

            try:
                print("Grille:")
                self.grillelogique.afficher_grille()
            except Exception as e:
                print("Erreur affichage grille:", e)

            try:
                self.grillelogique.draw_path(self.path)
            except Exception as e:
                print("Erreur draw_path:", e)

            self.EnnemiRectangle = pygame.Rect(self.EnnemiLogique.x*taillerow,self.EnnemiLogique.y*taillecol,taillerow,taillecol)
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
        for i in range(0,length,taillecol):
            for j in range(0,height,taillerow):
                rect = pygame.Rect((i,j),(taillerow,taillecol))
                pygame.draw.rect(surface,"Black",rect,1)
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
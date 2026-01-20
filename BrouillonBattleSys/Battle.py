import pygame
from BrouillonBattleSys.Pointetmatricelogique.EssaiPoint2D import Point2D, objet2D
from BrouillonBattleSys.Pointetmatricelogique.EssaiMatriceLogique import GrilleCombat
from BrouillonBattleSys.settingsBrouillonBS import *
from random import randint as rd

class Battle:
    def __init__(self):
        self.temps = 0
        self.screen = pygame.Surface((1000, 800))

        self.grillelogique = GrilleCombat(width//nrow, length//ncol)
        self.grillelogique.afficher_grille()
        self.grillegraphique = pygame.Rect((0,0),(length,width))

        self.taillecase = (width//nrow, length//ncol)
        print(length,width,ncol,nrow,self.taillecase)




        self.JoueurLogique = Point2D(0,0,"Joueur")
        self.JoueurRectangle = pygame.Rect(self.JoueurLogique.x,self.JoueurLogique.y,nrow,ncol)
        self.grillelogique.placer_element(self.JoueurLogique)

        self.EnnemiLogique = Point2D(70,70)
        self.EnnemiRectangle = pygame.Rect(self.EnnemiLogique.x*ncol,self.EnnemiLogique.y*nrow,nrow,ncol)
        self.grillelogique.placer_element(self.EnnemiLogique)

        self.Murs = []
        self.MursRect = []

        for i in range(0,3700,1):
            x, y = rd(1,69),rd(1,69)
            if x != self.EnnemiLogique.x and y!= self.EnnemiLogique.y:
                self.Murs.append(Point2D(x,y,f'Mur{i}'))
                self.MursRect.append(pygame.Rect(self.Murs[i].x*ncol,self.Murs[i].y*nrow,nrow,ncol))
            else:
                pass

        for mur in self.Murs:
            self.grillelogique.placer_element(mur)

        self.indicateur_path = False


        

        



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
                self.nomchemin = []
                self.pathRect = []
                for point in self.path:
                    self.pathRect.append(pygame.Rect(point.x*ncol,point.y*nrow,nrow,ncol))
                    

                    if point.element is None:
                        self.nomchemin.append(point.nom)
                    else:
                        self.nomchemin.append(point.element.nom)
                print(self.nomchemin)


    



    ### Horloge, fournira l'ATB et autres systemes temporels ###
    def horloge(self, dt):
        self.temps += dt
    


    ##### Partie graphique, elle appellera la partie logique #####
    ### Penser à caler la partie logique sur X fps, mais l'affichage a X/3 fps ###
    def draw(self, surface):
        surface.fill((255, 255, 255))
        font = pygame.font.Font(None, 20)
        text = font.render(f'Temps: {int(self.temps)}s', True, (0, 0, 0))
        pygame.draw.rect(surface,pygame.Color("Blue"),self.grillegraphique)

        ## Grille
        for i in range(0,length,ncol):
            for j in range(0,width,nrow):
                rect = pygame.Rect((i,j),(ncol,nrow))
                pygame.draw.rect(surface,"white",rect,1)
        pygame.draw.rect(surface,"purple",self.JoueurRectangle)
        pygame.draw.rect(surface,"yellow",self.EnnemiRectangle)
        for rect in self.MursRect:
            pygame.draw.rect(surface,"brown",rect)
        if self.indicateur_path == True:
            for point in self.pathRect:
                pygame.draw.rect(surface,"green",point)
        
        surface.blit(text, (0,0))
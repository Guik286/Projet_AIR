import pygame
from BrouillonBattleSys.settingsBrouillonBS import *





class EventementBattle:
    def __init__(self,event,matrice, acteurs):
        self.event = event #Evenement Pygame (event)
        self.matrice = matrice #Grille logique (matrice)
        self.acteurs = acteurs #Ensemble des acteurs (tuple/list)



    def Input_user(self):
        if self.controle.is_new_key_press("start") == True:
            self.path = []
            self.k = 0
            self.path = self.matrice.pathfinding(self.JoueurLogique,self.EnnemiLogique)
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
            self.controle.input = False

        elif self.controle.is_new_key_press("select"):
            self.pause_joueur = True
            if self.matrice.grid[9][9].element != self.EnnemiLogique:

                self.matrice.deplacer_element(self.EnnemiLogique,9,9)
                self.EnnemiRectangle = GO(self.EnnemiLogique).rectangle
                
            else:
                pass

        elif self.controle.is_new_key_press("A"):
            GA(self.JoueurLogique,self.matrice).attaque(self.EnnemiLogique)
            self.EnnemiRectangle = GO(self.EnnemiLogique).rectangle
        elif self.controle.is_key_down("X"):
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.path = []
                self.k = 0
                pos = pygame.math.Vector2(pygame.mouse.get_pos())
                self.xclick = int(pos.x//taillecol)
                self.yclick = int(pos.y//taillerow)
                self.IndMovePlayer = True
                ## On récupère la position du clic de la souris
                print(self.xclick,self.yclick)
                self.path = self.matrice.pathfinding(self.matrice.grid[self.xclick][self.yclick],self.JoueurLogique)
                #self.DeplaLogique.Mouvement(self.JoueurLogique,self.k,path)
                #self.matrice.deplacer_element(self.JoueurLogique,newx,newy)
                #self.JoueurRectangle = GO(self.JoueurLogique).rectangle
        elif self.controle.is_new_key_press("B"):
            self.EnnemiLogique.lp -=1
            self.EnnemiLogique.mort()
            print(f"Lp ennemi restant : {self.EnnemiLogique.lp}")
            if self.EnnemiLogique.Etat == "mort":
                self.matrice.retirer_element(self.EnnemiLogique.x,self.EnnemiLogique.y)
                self.matrice.print_element(self.EnnemiLogique.x,self.EnnemiLogique.y)
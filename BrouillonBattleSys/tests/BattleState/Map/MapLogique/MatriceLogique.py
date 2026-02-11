
#### Description temporaire des points et de la matrice de combat logique
import pygame
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from BrouillonBattleSys.settingsBrouillonBS import *
from math import sqrt
from BrouillonBattleSys.tests.BattleState.Entites.EntitesLogique.Player2D import Acteur
from BrouillonBattleSys.tests.BattleState.Entites.EntitesLogique.Point2D import Point2D
from queue import PriorityQueue


#### Tache : Proposer un support pour définir la position des objets, tracer les chemins à emprunter pour les animations

#### Fonctions :
## Creer un element (placer)
## Detruire un élément (retirer)
## Deplacer un élément [detruire puis creer]
## Path finding (trouver un chemin)

class GrilleCombat:
    ### Classe de la grille de combat logique
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.grid = [[Point2D(x, y) for y in range(hauteur)] for x in range(largeur)]
        self.grid[0][0].initialisation(self)  # Initialisation des éléments à None


    ## Element existe?

    def print_element(self, x, y):
        if self.grid[x][y].element is not None:
            print(self.grid[x][y].element.nom)
        else:
            print("Il n'y a aucun élément ici")



    ### Méthode pour placer un élément sur la grille
    def placer_element(self, element):
        x = element.x
        y = element.y
        if 0 <= x < self.largeur and 0 <= y < self.hauteur:
            self.grid[x][y].element = element
            element.x = x
            element.y = y
            print(f"l'élément ({x},{y}) a été placé")
        else:
            raise ValueError("Coordonnées hors de la grille")
        


    ### Méthode pour retirer un élément de la grille
    def retirer_element(self, x, y):
        if 0 <= x < self.largeur and 0 <= y < self.hauteur:
            self.grid[x][y].element = None
        else:
            raise ValueError("Coordonnées hors de la grille")
        

    ### Méthode pour déplacer un élément d'une position à une autre
    def deplacer_element(self, element, x2, y2):
        if not (0 <= x2 < self.largeur and 0 <= y2 < self.hauteur):
            raise ValueError("Coordonnées hors de la grille")
        if not self.grid[x2][y2].element:
            ## On peut garder en mémoire les différentes modifications apportés à l'élément ou duppliquer l'élément et effacer l'ancien. 
            ## On duplique l'élément à la nouvelle position (permet de garder l'état de l'élément en mémoire sur le script)
            self.grid[x2][y2].element = self.grid[element.x][element.y].element
            ## On efface l'ancien
            self.grid[element.x][element.y].element = None
            ## On met à jour les coordonnées de l'objet "élément"
            element.x = x2
            element.y = y2

        else:
            raise ValueError("La position cible est déjà occupée")
    

    ### On affiche toute la grille logique en l'état
    def afficher_grille(self):
        for row in self.grid:
            ligne = ""
            for point in row:
                if point.element is None:
                    ligne += "[ ]"
                else:
                    ligne += "[X]"
            print(ligne)

    ## Algo de pathfinding (à encapsuler ?)
    def pathfinding(self, start, end):
        # Implémentation simple de l'algorithme A*
        compte = 0
        EnsOuvert = PriorityQueue()
        # Use the grid cell objects for start/end to keep keys consistent
        start_cell = self.grid[start.x][start.y]
        end_cell = self.grid[end.x][end.y]

        EnsOuvert.put((0, compte, start_cell))
        came_from = {}
        g_score = {spot: float("inf") for row in self.grid for spot in row}
        g_score[start_cell] = 0
        f_score = {spot: float("inf") for row in self.grid for spot in row}
        f_score[start_cell] = sqrt((start_cell.x - end_cell.x) ** 2 + (start_cell.y - end_cell.y) ** 2)
        max_iterations = 1000  # Prevent infinite loop
        iteration_count = 0

        while not EnsOuvert.empty() and iteration_count < max_iterations:
            iteration_count += 1
            current = EnsOuvert.get()[2]
            # si on atteint le point d'arrive, on construit le chemin
            if current.x == end_cell.x and current.y == end_cell.y:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start_cell)
                path.reverse()
                return path  # Retourne le chemin trouvé

            for voisin in current.get_voisins(self):
                if voisin is None:
                    continue
                # cout_deplacement indexed as [dy+1][dx+1]
                dx = voisin.x - current.x
                dy = voisin.y - current.y
                cost = voisin.cout_deplacement[dx + 1][dy + 1]
                if cost is not None:
                    tentative_g_score = g_score[current] + cost

                    if tentative_g_score < g_score[voisin] and (not voisin.is_occupied() or (voisin.x == end_cell.x and voisin.y == end_cell.y)):
                        came_from[voisin] = current
                        g_score[voisin] = tentative_g_score
                        f_score[voisin] = tentative_g_score + sqrt((voisin.x - end_cell.x) ** 2 + (voisin.y - end_cell.y) ** 2)
                        if all(voisin != item[2] for item in EnsOuvert.queue):
                            compte += 1
                            EnsOuvert.put((f_score[voisin], compte, voisin))
        if iteration_count == max_iterations:
            print("Nombre max d'itération atteint")
        print("Pathfinding terminé") 
        

    
    def draw_path(self, path):
        for row in self.grid:
            ligne = ""
            for point in row:
                if point in path and point.element is None:
                    ligne += "[*]"
                elif point.element is None:
                    ligne += "[ ]"
                else:
                    ligne += "[X]"
            print(ligne)





        #algorithmeprincipal













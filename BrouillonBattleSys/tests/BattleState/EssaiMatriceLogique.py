
#### Description temporaire des points et de la matrice de combat logique
import pygame
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Data.settings import *
from math import sqrt
from Game_f.graphisme.states.acteurs.acteur import Acteur
from Game_f.mechs.logique.LogiqueCombat.Point2D import Point2D
from queue import PriorityQueue


class GrilleCombat:
    ### Classe de la grille de combat logique
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.grid = [[Point2D(x, y) for x in range(largeur)] for y in range(hauteur)]
        self.grid[0][0].initialisation(self)  # Initialisation des éléments à None


    ### Méthode pour placer un élément sur la grille
    def placer_element(self, element):
        x = element.x
        y = element.y
        if 0 <= x < self.largeur and 0 <= y < self.hauteur:
            self.grid[y][x].element = element
            element.x = x
            element.y = y
            print(f"l'élément ({x},{y}) a été placé")
        else:
            raise ValueError("Coordonnées hors de la grille")
        
    def print_element(self, x, y):
        if self.grid[y][x].element is not None:
            print(self.grid[y][x].element.nom)

    ### Méthode pour retirer un élément de la grille
    def retirer_element(self, x, y):
        if 0 <= x < self.largeur and 0 <= y < self.hauteur:
            self.grid[y][x].element = None
        else:
            raise ValueError("Coordonnées hors de la grille")
    ### Méthode pour déplacer un élément d'une position à une autre
    def deplacer_element(self, element, x2, y2):
        if not (0 <= x2 < self.largeur and 0 <= y2 < self.hauteur):
            raise ValueError("Coordonnées hors de la grille")
        if not self.grid[y2][x2].element:
            if element:
                self.retirer_element(element.x, element.y)
                element.x = x2
                element.y = y2
                self.placer_element(element)
            else:
                raise ValueError("L'élément à déplacer n'existe pas")
        else:
            raise ValueError("La position cible est déjà occupée")
    
    def afficher_grille(self):
        for row in self.grid:
            ligne = ""
            for point in row:
                if point.element is None:
                    ligne += "[ ]"
                else:
                    ligne += "[X]"
            print(ligne)

    def pathfinding(self, start, end):
        # Implémentation simple de l'algorithme A* ou Dijkstra pourrait être ajoutée ici
        compte = 0
        EnsOuvert = PriorityQueue()
        # Use the grid cell objects for start/end to keep keys consistent
        start_cell = self.grid[start.y][start.x]
        end_cell = self.grid[end.y][end.x]

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
                cost = voisin.cout_deplacement[dy + 1][dx + 1]
                if cost is not None:
                    tentative_g_score = g_score[current] + cost

                    if tentative_g_score < g_score[voisin] and (not voisin.is_occupied() or (voisin.x == end_cell.x and voisin.y == end_cell.y)):
                        came_from[voisin] = current
                        g_score[voisin] = tentative_g_score
                        f_score[voisin] = tentative_g_score + sqrt((voisin.x - end_cell.x) ** 2 + (voisin.y - end_cell.y) ** 2)
                        if all(voisin != item[2] for item in EnsOuvert.queue):
                            compte += 1
                            EnsOuvert.put((f_score[voisin], compte, voisin))

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













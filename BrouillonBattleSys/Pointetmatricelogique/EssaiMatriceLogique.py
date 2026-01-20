
#### Description temporaire des points et de la matrice de combat logique
import pygame
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
        print(self.largeur,self.hauteur)

    ### Méthode pour placer un élément sur la grille
    def placer_element(self, element):
        x = element.x
        y = element.y
        if 0 <= x < self.largeur and 0 <= y < self.hauteur:
            self.grid[y][x].element = element
            element.x = x
            element.y = y
        else:
            raise ValueError("Coordonnées hors de la grille")

    ### Méthode pour retirer un élément de la grille
    def retirer_element(self, x, y):
        if 0 <= x < self.largeur and 0 <= y < self.hauteur:
            self.grid[y][x].element = None
        else:
            raise ValueError("Coordonnées hors de la grille")
    ### Méthode pour déplacer un élément d'une position à une autre
    def deplacer_element(self, element, x2, y2):
        if not self.grid[x2][y2].element:
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
        EnsOuvert.put((0, compte, start))
        came_from = {}
        g_score = {spot: float("inf") for row in self.grid for spot in row}
        g_score[start] = 0
        f_score = {spot: float("inf") for row in self.grid for spot in row}
        f_score[start] = sqrt((start.x - end.x) ** 2 + (start.y - end.y) ** 2)
        print(EnsOuvert.empty())
        print(end)

        while not EnsOuvert.empty():
            current = EnsOuvert.get()[2]
            print(f"Visiting point: ({current.x}, {current.y})")
            #si on atteint le point d'arrive, on construit le chemin
            if current.x == end.x and current.y == end.y:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path  # Retourne le chemin trouvé
            

            for voisin in current.get_voisins(self):    
                if voisin and voisin.cout_deplacement[current.x - voisin.x + 1][current.y - voisin.y + 1] is not None:
                    tentative_g_score = g_score[current] + voisin.cout_deplacement[current.x - voisin.x + 1][current.y - voisin.y + 1]

                    if tentative_g_score < g_score[voisin] and (not voisin.is_occupied() or (voisin.x == end.x and voisin.y == end.y)):
                        came_from[voisin] = current
                        g_score[voisin] = tentative_g_score
                        f_score[voisin] = tentative_g_score + sqrt((voisin.x - end.x) ** 2 + (voisin.y - end.y) ** 2)
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













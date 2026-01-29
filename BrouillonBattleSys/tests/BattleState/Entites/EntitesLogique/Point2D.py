#### Classes des points et de la matrice de combat logique ####
import pygame
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Data.settings import *

class Point2D:
    ### Un point sert de support aux classes filles, il permet de gérer les coordonnées
    def __init__(self, x, y, nom="Point"):
        self.x = x
        self.y = y
        self.nom = nom
        if self.nom == 'Point':
            self.nom = f"Point ({self.x},{self.y})"
        self.element = None  # Élément placé sur ce point
        self.voisins = [[None for _ in range(3)] for _ in range(3)]  # Matrice des voisins
        self.cout_deplacement = [[1.4,1,1.4],[1,0,1],[1.4,1,1.4]]  # Coût de déplacement vers chaque voisin
        self.initialisee = False
          # Coût de déplacement par défaut

    def initialisation(self, grille):
        self.initialisee = True
        self.get_voisins(grille)

    def __eq__(self, other):
        if not isinstance(other, Point2D):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def is_occupied(self):
        return self.element is not None
    
    #def is_item(self):
    #    return isinstance(self.element, objet2D)
    #
    #def is_actor(self):
    #    return isinstance(self.element, Acteur)

    ### Méthode de déplacement du point (autoriser diagonale)
    def deplacer(self, dx, dy):
        self.x += dx
        self.y += dy
        return (self.x, self.y)
    
    ### Pour le pathfinding il devra connaitre ses voisins

    def get_voisins(self, grille):
        self.voisins = [grille.grid[self.x + dx][self.y + dy] if 0 <= self.x + dx < grille.largeur and 0 <= self.y + dy < grille.hauteur else None
                        for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx != 0 or dy != 0)]

        return self.voisins
    

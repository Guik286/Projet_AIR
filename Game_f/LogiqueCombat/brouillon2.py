
#### Description temporaire des points et de la matrice de combat logique
import pygame
from Data.settings import *
from math import sqrt
from Game_f.states.acteurs.acteur import Acteur
from queue import PriorityQueue


class GrilleCombat:
    ### Classe de la grille de combat logique
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille = [[Point2D(x, y) for x in range(largeur)] for y in range(hauteur)]
        self.grille[0][0].initialisation(self)  # Initialisation des éléments à None

    ### Méthode pour placer un élément sur la grille
    def placer_element(self, element):
        x = element.x
        y = element.y
        if 0 <= x < self.largeur and 0 <= y < self.hauteur:
            self.grille[y][x].element = element
            element.x = x
            element.y = y
        else:
            raise ValueError("Coordonnées hors de la grille")

    ### Méthode pour retirer un élément de la grille
    def retirer_element(self, x, y):
        if 0 <= x < self.largeur and 0 <= y < self.hauteur:
            self.grille[y][x].element = None
        else:
            raise ValueError("Coordonnées hors de la grille")
    ### Méthode pour déplacer un élément d'une position à une autre
    def deplacer_element(self, element, x2, y2):
        if not self.grille[x2][y2].element:
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
        for row in self.grille:
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
        origine = {}
        g_score = {point: float("inf") for row in self.grille for point in row}
        g_score[start] = 0 
        f_score = {point: float("inf") for row in self.grille for point in row}
        f_score[start] = self.heuristique(start, end)


        #algorithmeprincipal





#### Classes des points et de la matrice de combat logique ####
class Point2D:
    ### Un point sert de support aux classes filles, il permet de gérer les coordonnées
    def __init__(self, x, y, nom="Point"):
        self.x = x
        self.y = y
        self.nom = nom
        self.element = None  # Élément placé sur ce point
        self.voisins = [[None for _ in range(3)] for _ in range(3)]  # Matrice des voisins
        self.cout_deplacement = [[1.4,1,1.4],[1,0,1],[1.4,1,1.4]]  # Coût de déplacement vers chaque voisin
        self.initialisee = False
          # Coût de déplacement par défaut

    def initialisation(self, grille):
        self.initialisee = True
        self.get_voisins(grille)

    def is_occupied(self):
        return self.element is not None

    ### Méthode de déplacement du point (autoriser diagonale)
    def deplacer(self, dx, dy):
        self.x += dx
        self.y += dy
        return (self.x, self.y)
    
    ### Pour le pathfinding il devra connaitre ses voisins

    def get_voisins(self, grille):
        self.voisins = []
        dx = range(-1,1,1)
        dy = range(-1,1,1)
          # Haut, Bas, Gauche, Droite et Diagonales
        
        for x in dx:
            for y in dy:
                if x != 0 or y != 0:
                    nx, ny = self.x + x, self.y + y
                    if 0 <= nx < grille.largeur and 0 <= ny < grille.hauteur:
                        self.voisins[nx][ny] = grille.grille[ny][nx]
                        if self.voisins[nx][ny].initialisee == True:
                            pass
                        else: self.voisins[nx][ny].initialisation(grille)
                    else:
                        self.cout_deplacement[nx][ny] = None  # Hors de la grille
                else:
                    continue

        return self.voisins
    
## Classe fille des points, un objet est un point avec des propriétés supplémentaires
class objet2D(Point2D):
    ### Classe fille de point2D, un objet est un point avec des propriétés supplémentaires
    def __init__(self, x, y, nom, description, lp=1,defense = 1):
        super(objet2D,self).__init__(x, y)
        self.nom = nom
        self.description = description
        self.lp = lp
        self.defense = defense

### Classe fille des objets, un acteur est un objet avec des statistiques de combat
class Acteur(objet2D):
    def __init__(self, x, y, nom, description, lp=100, defense=10):
        super(Acteur,self).__init__(x, y, nom, description, lp, defense)
        self.nom = nom
        self.description = description
        self.lp = lp
        self.defense = defense





matrice = GrilleCombat(20,18)
D = Point2D(0,0,"D")
A = Point2D(4,0,"A")

matrice.placer_element(D)
matrice.placer_element(A)
matrice.afficher_grille()
matrice.deplacer_element(A,20,18)


print(matrice.grille[0][0].element.nom)





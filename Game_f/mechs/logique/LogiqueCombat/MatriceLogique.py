
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
        self.voisins = [grille.grid[self.y + dy][self.x + dx] if 0 <= self.x + dx < grille.largeur and 0 <= self.y + dy < grille.hauteur else None
                        for dy in [-1, 0, 1] for dx in [-1, 0, 1] if (dx != 0 or dy != 0)]

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
A = Point2D(5,0,"A")
M = Point2D(1,0,"Mur")
M2 = Point2D(1,1,"Mur2")
M3 = Point2D(1,2,"Mur3")
M4 = Point2D(1,3,"Mur4")
M5 = Point2D(1,4,"Mur5")

M6 = Point2D(3,4,"Mur6")
M7 = Point2D(3,3,"Mur7")
M8 = Point2D(3,2,"Mur8")
M9 = Point2D(3,1,"Mur9")


matrice.placer_element(D)
matrice.placer_element(A)
matrice.placer_element(M)
matrice.placer_element(M2)
matrice.placer_element(M3)
matrice.placer_element(M4)
matrice.placer_element(M5)
matrice.placer_element(M6)
matrice.placer_element(M7)
matrice.placer_element(M8)
matrice.placer_element(M9)





matrice.afficher_grille()

path = matrice.pathfinding(D,A)
nomchemin = []
for point in path:
    if point.element is None:
        nomchemin.append(point.nom)
    else:
        nomchemin.append(point.element.nom)

print(nomchemin)

matrice.draw_path(path if path else [])
print(path)







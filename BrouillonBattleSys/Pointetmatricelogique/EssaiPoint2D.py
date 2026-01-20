#### Classes des points et de la matrice de combat logique ####
import pygame
from Data.settings import *

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
    
    def is_item(self):
        return isinstance(self.element, objet2D)
    
    def is_actor(self):
        return isinstance(self.element, Acteur)

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
    def __init__(self, x, y, nom, description, lp_max = 1,defense = 1,Etat = "no_alt",Image=None):
        super(objet2D,self).__init__(x, y)
        self.nom = nom
        self.description = description
        #Statistiques de l'objet
        self.lp_max = lp_max
        self.lp = lp_max
        self.defense = defense
        #Image et rectangle de l'objet
        self.image = Image
        self.rect = pygame.Rect(x,y,taillecase,taillecase)
        if self.image is not None:
            self.rect_img = self.image.get_rect()
            self.rect_img.center = self.rect.center
        self.Etat = Etat  # Etat de l'objet (ex: "no_alt", "altéré", "cassé", etc.)
        self.hit = False



    def mort(self):
        if self.lp <= 0:
            self.lp = 0
            self.Etat = "mort"
            print(f"{self.nom} est mort.")

    def Recevoir_degats(self, degats):
        self.lp -= degats
        print(f"{self.nom} a reçu {degats} points de dégâts. Points de vie restants : {self.lp}")
        if self.lp <= 0:
            self.mort()
        # Actions supplémentaires à la mort de l'objet peuvent être ajoutées ici

### Classe fille des objets, un acteur est un objet avec des statistiques de combat
class Acteur(objet2D):
    def __init__(self, x, y, nom, description, lp=100, defense=10):
        super(Acteur,self).__init__(x, y, nom, description, lp, defense)
        self.nom = nom
        self.description = description
        self.lp = lp
        self.defense = defense

        


from math import sqrt
import pygame
from settingsBrouillonBS import *
import random as rd


class RegleCombat:
    ### Classe des règles de combat
    def __init__(self,liste_acteurs):
        self.liste_acteurs = liste_acteurs
        self.result = -1


    def tirer_des(self):
        self.result = rd.randint(0,99)
        return self.result

    def tirer_initiative(self):
        ### Tirage d'initiative pour chaque acteur
        i = 0
        acteurs_actuel = []
        self.liste_acteurs.sort(key=lambda x: x.vit, reverse=True) ## On oragnise la liste en fonction de la vitesse
        for j in range (1,len(self.liste_acteurs)-1,1):
            # On garde les acteurs avec la même vitesse et on tire un dés pour chacun

            if self.liste_acteurs[j].vit == self.liste_acteurs[i].vit:
                acteurs_actuel.append(self.liste_acteurs[j])
            else:
                i += len(acteurs_actuel) ## on garde l'info pour reprendre la boucle plus tard
                # Tirage de dés pour les acteurs actuels
                for a in acteurs_actuel:
                    a.initiative = a.vit + self.tirer_des()
                acteurs_actuel = [] #On renitialise la liste pour le prochain groupe

        # Tri des acteurs par initiative décroissante
        self.liste_acteurs.sort(key=lambda x: x.initiative, reverse=True)
        return self.liste_acteurs
        


class EffetSpatiaux:
    ##### Effet de déplacement d'un point sur la matrice
    def __init__(self,Matrice):
        self.matrice = Matrice

    def Knockback(self,cible,source):
        ### Direction 
        direction = ((cible.x - source.x),(cible.y-source.y))
        if direction[0] != 0:
            newx = cible.x + int(direction[0]/sqrt((cible.x-source.x)**2 ))
        else:
            newx = cible.x
        if direction[1] !=0 : 

            newy = cible.y + int(direction[1]/sqrt((cible.y-source.y)**2))
        else:
            newy = cible.y
        if self.matrice.grid[newx][newy].is_occupied():
            pass
        else:
            self.matrice.deplacer_element(cible,newx,newy)
            cible.x = newx
            cible.y = newy
        #self.EnnemiRectangle = pygame.Rect(cible.x * taillecol, cible.y * taillerow, taillecol, taillerow)

    def Mouvement(self,point,indice,path):
        longueur_chemin = len(path) ## Longueur du path a suivre pour l'indexation
        print(f"la longueur du chemin est:{longueur_chemin}")
        case_actuelle = path[longueur_chemin -min(indice,longueur_chemin)] ### Pour ordre décroissant et stop a longueur chemin (s'arrête a 1)
        x = case_actuelle.x
        y = case_actuelle.y
        try:
            self.matrice.deplacer_element(point, x, y)
            print(f"L'indice d'évolution sur le chemin est :{indice}")
                
        except ValueError as e:
            print(f"Déplacement impossible vers ({x},{y}) : {e}")
            print(f"L'indice d'évolution sur le chemin est :{indice}")

    



class GraphObjet:
    def __init__(self,objet):

            self.objet = objet
            self.image = objet.image
            self.rectangle = pygame.Rect(objet.x * taillecol,objet.y * taillerow, taillecol,taillerow)

    def Dessiner_Objet(self,surface):
            if self.objet.nom == "Joueur":
                pygame.draw.rect(surface,pygame.Color("Purple"),self.rectangle)
            else:     
                pygame.draw.rect(surface,pygame.Color("Yellow"),self.rectangle)




class Gestion_Acteur:
    def __init__(self,acteur,matrice):
        self.acteur = acteur
        self.space = EffetSpatiaux(matrice)


    def attaque(self,cible):
        A = self.acteur.atq
        D = cible.defense

        if A > D :
            self.space.Knockback(cible,self.acteur)
            cible.Recevoir_degats(0)
        else:
            pass
    
    def Pos_defensive(self):
        self.acteur.defense += 5
        print(f"La défense de {self.acteur.nom} augmente à {self.acteur.defense}")

    






        
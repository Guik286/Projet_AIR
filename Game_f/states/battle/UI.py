import pygame


from Game_f.states.acteurs.acteur import Acteur

class UI:
    def __init__(self,acteur):
        ### Faire une barre de vie pour l'acteur a afficher en dessous de l'acteur
        self.acteur = acteur
        self.barre_vie = pygame.Rect((acteur.rect.x,acteur.rect.y + acteur.rect.height + 30),(acteur.rect.width,10))


    def lifebar(self,surface):
        ### Dessine la barre de vie de l'acteur
        pygame.draw.rect(surface,(255,0,0),self.barre_vie)
        vie_ratio = self.acteur.lp / self.acteur.lp_max  ## A modifier en fonction des LP max
        pygame.draw.rect(surface,(0,255,0),(self.barre_vie.x,self.barre_vie.y,self.barre_vie.width * vie_ratio,self.barre_vie.height))
import pygame


from Game_f.states.acteurs.acteur import Acteur

class UI:
    def __init__(self,acteur):
        ### Faire une barre de vie pour l'acteur a afficher en dessous de l'acteur
        self.acteur = acteur
        self.barre_vie = pygame.Rect((acteur.rect.x,acteur.rect.y + acteur.rect.height + 30),(acteur.rect.width,10))

        self.dommage_pop = pygame


    def lifebar(self,surface):
        ### Dessine la barre de vie de l'acteur
        pygame.draw.rect(surface,(255,0,0),self.barre_vie)
        vie_ratio = self.acteur.lp / self.acteur.lp_max  ## A modifier en fonction des LP max
        pygame.draw.rect(surface,(0,255,0),(self.barre_vie.x,self.barre_vie.y,self.barre_vie.width * vie_ratio,self.barre_vie.height))

    def display_damage(self,surface):

        if self.acteur.hit > 0:
            font = pygame.font.SysFont('arial',self.acteur.hit * 5 + 20)
            damage_text = font.render(str(self.acteur.damage),True,(255,255,255))
            surface.blit(damage_text,(self.acteur.rect.x + self.acteur.rect.width // 2 - damage_text.get_width() // 2,
                                     self.acteur.rect.y - 20 - (self.acteur.hit * 5)))
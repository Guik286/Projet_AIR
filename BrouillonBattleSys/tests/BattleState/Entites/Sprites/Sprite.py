import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super(Sprite, self).__init__()
        self.image = image
        self.position = position
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
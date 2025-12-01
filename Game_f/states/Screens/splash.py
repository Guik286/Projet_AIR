import pygame
from Game_f.states.base import BaseState


class Splash(BaseState):
    def __init__(self):
        super(Splash, self).__init__()
        self.next_state = "MENU"
        self.time_active = 0
        self.largeText = pygame.font.Font('Data/font/lycheesoda.ttf',200)
        self.Surf_Text, self.Rect_Text = self.text_object("Chapitre 1", self.largeText)
        self.Rect_Text.center = (960,150)
        self.loaded_image = pygame.image.load('Data/graphics/BackgroundTitle/AIR_Background.png')
        
        
    def text_object(self,text,font):
        TextSurf = font.render(text,True,(0,0,255))
        return TextSurf, TextSurf.get_rect()

    def update(self, dt):
        self.time_active += dt
        if self.time_active >= 1:
            self.done = True

    def draw(self, surface):
        
        surface.fill(pygame.Color("black"))
        
        surface.blit(self.loaded_image,(0,0))
        
        surface.blit(self.Surf_Text, self.Rect_Text)
import pygame
from Game_f.states.base import BaseState



class Ecran_Victoire(BaseState):
    def __init__(self):
        super(Ecran_Victoire, self).__init__()
        self.next_state = "MENU"
        self.largeText = pygame.font.SysFont('Arial',200)
        self.Surf_Text, self.Rect_Text = self.text_object("Victoire !!!", self.largeText)
        self.Rect_Text.center = (960,150)


    def text_object(self,text,font):
        TextSurf = font.render(text,True,(0,0,255))
        return TextSurf, TextSurf.get_rect()
    
    def get_event(self,event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_0:
                self.done = True

    def draw(self, surface):
        
        surface.fill(pygame.Color("black"))
        
        
        surface.blit(self.Surf_Text, self.Rect_Text)
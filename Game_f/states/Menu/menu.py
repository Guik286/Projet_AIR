import pygame
from GI import GraphicInterface
from Game_f.states.base import BaseState





class Menu(BaseState):
    def __init__(self):
        super(Menu, self).__init__()
        self.active_index = 0
        self.options = ["New Game","Load Game","Options","Quit"]
    

        
        
        
        ### Selection des options

    #def render_text(self, index):
    #    color = pygame.Color("red") if index == self.active_index else pygame.Color("white")
    #    return self.font.render(self.options[index], True, color)
#
    #def get_text_position(self, text, index):
    #    center = (self.screen_rect.center[0], self.screen_rect.center[1] + (index * 50))
    #    return text.get_rect(center=center)

    def handle_action(self):
        if self.active_index == 0:
            self.next_state = "GAMEPLAY"
            self.done = True
        elif self.active_index == 1:
            pass
        elif self.active_index == 2:
            self.next_state = "Options"
            self.done = True
        
        elif self.active_index == 3:
            self.quit = True
        

    ## Gerer les controles
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.active_index <=0:
                    self.active_index = 3
                else:
                    self.active_index -= 1
            elif event.key == pygame.K_DOWN:
                if self.active_index >= 3:
                    self.active_index = 0
                else:
                    self.active_index +=1
            elif event.key == pygame.K_RETURN:
                self.handle_action()
    ## Dessin
    
    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        GraphicInterface(self.options,self.active_index,self.screen_rect).draw(surface)
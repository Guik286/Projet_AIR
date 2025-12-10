import pygame
from Game_f.states.base import BaseState
from GI import GraphicInterface

class Options(BaseState):
    def __init__(self):
        super(Options, self).__init__()
        self.active_index = 0
        self.choix = ["Retour au Menu" , "Volume :" ]
        self.Vol_Bar = pygame.Rect(300,500,500,40)

        self.Music_Test = pygame.mixer.Sound('Data/audio/gnosiaop.mp3')
        self.Music_Test.set_volume(0)
        self.Music_Test.play(loops = -1)

        self.Vol_Actuel = self.Music_Test.get_volume()
        

        
    


    def Action(self):
        if self.active_index ==0:
            self.next_state = "MENU"
            self.done = True


        ## Gerer les controles
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.active_index <= 0:
                    self.active_index = 1
                else:
                    self.active_index -= 1
            elif event.key == pygame.K_DOWN:
                if self.active_index >= 1:
                    self.active_index = 0
                else:
                    self.active_index +=1
            elif event.key == pygame.K_RETURN and self.active_index != 1:
                self.Action()
            elif self.active_index == 1 and event.key == pygame.K_RIGHT:
                self.Vol_Actuel += 0.01
                self.Music_Test.set_volume(self.Vol_Actuel)

            elif self.active_index == 1 and event.key == pygame.K_LEFT:
                self.Vol_Actuel -= 0.01
                self.Music_Test.set_volume(self.Vol_Actuel)

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        ## Texte 
        GraphicInterface(self.choix,self.active_index,self.screen_rect).draw(surface)

        ## Barre Volume: 
        ratio = self.Vol_Actuel * 5000/self.Vol_Bar.width
        larg_act = self.Vol_Bar.width * ratio
        rect_actuel = self.Vol_Bar.copy()
        rect_actuel.width = larg_act

        #Dessin arriere plan 
        pygame.draw.rect(pygame.display.get_surface(),'black',self.Vol_Bar)

        ##Dessin de la barre 
        pygame.draw.rect(pygame.display.get_surface(),'white',self.Vol_Bar,3)
        pygame.draw.rect(pygame.display.get_surface(),'red',rect_actuel)
        



import pygame
from KeysManager import KeysManager

class Game:
    def __init__(self, screen, states, initial_state):
        self.screen = screen
        self.states = states
        self.current_state = states[initial_state]

        ### Mappage des controles
        self.current_state.controle = KeysManager()
        ## Indicateur de pause (buffer?)



    def maj_horloge(self, dt):
        self.current_state.horloge(dt)


    def Affichage(self):
        self.current_state.draw(self.screen)
        pygame.display.flip()

    def evenements(self):
        self.current_state.controle._last_keys = self.current_state.controle._new_keys.copy()
        for event in pygame.event.get():
            self.current_state.get_event(event)
            self.current_state.controle.Gestion_evenement(event)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))
            self.maj_horloge(pygame.time.Clock().tick(60))
            self.Affichage()
            self.evenements()
            pygame.display.update()
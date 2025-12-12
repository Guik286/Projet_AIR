import pygame
from Game_f.states.battle.Battlescreen import Level



class Game(object):
    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

        
        

    def event_loop(self):
        for event in pygame.event.get():
            self.state.get_event(event)

    def flip_state(self):
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)




    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)


    def draw(self):
        self.state.draw(self.screen)

    def run(self):

        while not self.done:
            if self.state_name == "Victoire":
                print("Reinitialisation du niveau...")
                self.states["GAMEPLAY"].done = False

                Level().__init__()  ## Reinitialisation du niveau pour le joueur

            dt = self.clock.tick() /1000
            self.event_loop()
            self.update(dt)
            self.draw()
            pygame.display.update()


            
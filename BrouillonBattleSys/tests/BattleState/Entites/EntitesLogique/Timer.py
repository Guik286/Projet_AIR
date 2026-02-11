from settingsBrouillonBS import *


class Timer:
    def __init__(self, duration):
        self.start_time = 0
        self.duration = duration
        self.active = False
        self.current_time = 0
        
    def __bool__(self):
        return self.active
    
    def activer(self):
        self.start_time = pygame.time.get_ticks()
        self.active = True
    
    def desactiver(self):
        self.active = False
        self.start_time = 0

    def update(self):
        if self.active:
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.start_time >= self.duration:
                self.desactiver()
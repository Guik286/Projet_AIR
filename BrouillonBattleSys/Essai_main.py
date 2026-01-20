import pygame
import sys

from BrouillonBattleSys.Game import Game


from BrouillonBattleSys.settingsBrouillonBS import length, width
from BrouillonBattleSys.Battle import Battle


pygame.init()

screen = pygame.display.set_mode((length, width))
states = {"Battle" : Battle()}

game = Game( screen, states, "Battle")
game.run()

### Indicatrice de mise sous tension

pygame.quit()
sys.exit()
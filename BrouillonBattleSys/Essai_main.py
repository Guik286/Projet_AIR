import pygame
import sys

from Game import Game


from settingsBrouillonBS import length, height
from BrouillonBattleSys.tests.BattleState.Battlemain import Battle


pygame.init()
### Definition de l'image
screen = pygame.display.set_mode((length, height))


## Dictionnaire des écrans
states = {"Battle" : Battle()}



game = Game( screen, states, "Battle")
game.run()

### Indicatrice de mise sous tension

pygame.quit()
sys.exit()
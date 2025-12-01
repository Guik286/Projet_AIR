import pygame, sys

#### Classe de gestion des screens
from Game_f.Game import Game
### Menus et options
from Game_f.states.Menu.menu import Menu
from Game_f.states.Menu.options import Options

### Ecrans de jeu

from Game_f.states.Screens.splash import Splash
from Game_f.states.battle.Battlescreen import Level
from Game_f.states.Screens.Screen_Victoire import Ecran_Victoire
from Game_f.states.Screens.game_over import GameOver

### Config

from Data.settings import *

pygame.init()

screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
states = {
    "MENU" : Menu(),
    "SPLASH" : Splash(),
    "GAMEPLAY" : Level(),
    "GAME_OVER" : GameOver(),
    "Options" : Options(),
    "Victoire" : Ecran_Victoire()

}

game = Game(screen,states,"SPLASH")
game.run()

pygame.quit()
sys.exit()


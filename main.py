import pygame, sys
from states.Menu.menu import Menu
from states.Menu.game_over import GameOver
from states.Menu.splash import Splash
from states.Menu.options import Options
from Game import Game
from states.battlescreen.Battlescreen import Level
from states.battlescreen.Screen_Victoire import Ecran_Victoire

from states.battlescreen.ATB import *

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


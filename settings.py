import pygame as pg
from os import path
pg.init()
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
GRAY=(220,220,220)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN=(0,255,255)
DARKBLUE=(0,0,49)
PURPLE=(172,79,198)
BLUE=(0,0,255)
BGCOLOR = DARKGREY
NIGHTCOLOR=(20, 20, 20)

# game settings
WIDTH = pg.display.Info().current_w
HEIGHT =pg.display.Info().current_h
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

NORTH=0
SOUTH=1
EAST=2
WEST=3

# default_font
game_folder = path.dirname(__file__)
FONT=path.join(game_folder+"/"+"PixelColeco-4vJW.ttf")
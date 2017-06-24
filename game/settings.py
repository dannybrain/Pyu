''' Pyu, a simple platformer game made in Pygame

Inspired by the wonderful KidsCanCode videos on youtube
'''
import os

# PYGAME settings
# Frame per seconds
FPS = 60

# FILES
# to keep columns short enough to comply with pep8 when
# graphics are loaded, needed to create a EXPLOD_PATH constant
FILE_PATH = os.path.dirname('__file__')
IMG_PATH = os.path.join(FILE_PATH, 'img')
SND_PATH = os.path.join(FILE_PATH, 'snd')
# FONT_NAME = pg.font.match_font('arial')

# WINDOW
WIDTH = 800
HEIGHT = 600

# GAME
TITLE = "PYU"
VELOCITY_MAX = 7.0
ACCELERATION_MAX = 2.5

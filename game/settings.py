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
SPRITESHEET_FILE = 'spritesheet_jumper.png'
# FONT_NAME = pg.font.match_font('arial')

# WINDOW
WIDTH = 800
HEIGHT = 600

# GAME
BGCOLOR = (0, 155, 155)
BLACK = (0, 0, 0)
TITLE = "PYU"
PLAYER_FRICTION = -0.12
PLAYER_ACCEL = 0.5
PLAYER_GRAVITY = 0.8
PLAYER_JMP_FORCE = -20
PLAYER_JMP_CUT = -6
POWER_UP_PCT = 7
POWER_UP_JMP_FORCE = -50
IDLE_ANIMATION_SPEED = 300
WALKING_ANIMATION_SPEED = 150
PLATFORM_LIST = [(300, 400, 150, 20),
                 (400, 300, 50, 20),
                 (150, 100, 200, 20),
                 (180, 200, 100, 20),
                 (200, 500, 50, 20),
                 (400, 500, 50, 20),
                 (600, 500, 50, 20),
                 (600, 220, 175, 20),
                 (550, 120, 100, 20),
                 (0, HEIGHT - 80, WIDTH, 40)]

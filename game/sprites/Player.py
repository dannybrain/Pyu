import pygame as pg
from webcolors import name_to_rgb as rgb

from settings import *

# redefine/shorten vector definition
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, 30))
        self.image.fill(rgb('yellow'))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

    def update(self):
        self.acceleration = vec(0, 0)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acceleration = vec(-.5, 0)
        if keys[pg.K_RIGHT]:
            self.acceleration = vec(.5, 0)

        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        self.rect.center = self.position


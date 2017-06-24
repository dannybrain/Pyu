import pygame as pg
from webcolors import name_to_rgb as rgb


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height))
        self.image.fill(rgb('green'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

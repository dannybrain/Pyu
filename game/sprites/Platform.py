import pygame as pg
from random import choice


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = [game.spritesheet.get_image(213, 1662, 201, 100),
                       game.spritesheet.get_image(0, 288, 380, 94)]
        self.image = choice(self.images)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

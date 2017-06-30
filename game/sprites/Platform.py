import pygame as pg


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = game.spritesheet.get_image(
            x=0,
            y=96,
            width=380,
            height=94
        )
        self.image = pg.transform.scale(self.image, (95, 23))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

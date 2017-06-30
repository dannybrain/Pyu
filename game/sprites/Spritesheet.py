import pygame as pg


class Spritesheet():
    def __init__(self, file):
        self.image = pg.image.load(file).convert()

    def get_image(self, x, y, width, height):
        ''' get a slice of the spritesheet '''
        image = pg.Surface((width, height))
        image.blit(self.image,
                   (0, 0),
                   (x, y, width, height))
        return image

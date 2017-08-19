import pygame as pg
''' Powerup sprite class '''


class Pow(pg.sprite.Sprite):
    def __init__(self, game, target_platform):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        image = game.spritesheet.get_image(434, 1265, 145, 110)
        self.image = pg.transform.scale(image, (36, 27))
        self.image.set_colorkey((0, 0, 0))
        self.plat = target_platform
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 1

    def update(self):
        self.rect.bottom = self.plat.rect.top - 1
        # if the platform is no longer shown on screen, there is
        # no reason to keep the powerup either !
        if not self.game.platforms.has(self.plat):
            self.kill()

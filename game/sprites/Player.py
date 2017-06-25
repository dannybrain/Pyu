import pygame as pg
from webcolors import name_to_rgb as rgb

from settings import *

# redefine/shorten vector definition
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((40, 30))
        self.image.fill(rgb('yellow'))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

    def jump(self):
        # jump only if staying on top of a platform
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            self.velocity.y = PLAYER_JMP_FORCE

    def update(self):
        self.acceleration = vec(0, PLAYER_GRAVITY)

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acceleration.x = -PLAYER_ACCEL
        if keys[pg.K_RIGHT]:
            self.acceleration.x = PLAYER_ACCEL

        # friction slows down the acceleration a bit
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION
        # equation of motion
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        # check edges
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x <= 0:
            self.position.x = WIDTH - self.rect.width / 2

        self.rect.midbottom = self.position

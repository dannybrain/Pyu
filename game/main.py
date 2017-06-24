#!/usr/bin/env python3
''' Pyu, a simple platformer game made in Pygame

Inspired by the wonderful KidsCanCode videos on youtube
'''
import sys
import pygame as pg
from webcolors import name_to_rgb as rgb

from settings import *
from sprites.Player import Player
from sprites.Platform import Platform


class Game(object):
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        # Load graphics and sound
        self._load_gfx()
        self._load_snd()
        # Running indicates the game is in an active state
        self.running = True

    def new(self):
        ''' start up a brand new game '''
        # Create group and sprites
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for platform in PLATFORM_LIST:
            p = Platform(*platform)
            self.platforms.add(p)
            self.all_sprites.add(p)

        # Play background music and let's get started !
        # pg.mixer.music.play(loops=-1)
        self.run()

    def run(self):
        ''' main game loop after initialization '''
        # Playing indicates the game has actually started
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.draw()
            self.events()
            self.update()
            # Loop condition to end the game

    def draw(self):
        ''' draw objects on screen '''
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)

        # debug information
        Game.draw_text(
            self.screen,
            "Velocity = ({}, {})".format(
                round(self.player.velocity.x),
                round(self.player.velocity.y)
            ),
            20,
            (90, 10)
        )

        Game.draw_text(
            self.screen,
            "Acceleration = ({}, {})".format(
                round(self.player.acceleration.x),
                round(self.player.acceleration.y)
            ),
            20,
            (90, 40)
        )

        Game.draw_text(
            self.screen,
            "collide = " + str(len(pg.sprite.spritecollide(
                self.player,
                self.platforms,
                False))),
            20,
            (90, 70)
        )

        # after drawing everything, flip
        pg.display.flip()

    def _detect_collisions(self):
        self._player_with_platform_collision()

    def _player_with_platform_collision(self):
        hits = pg.sprite.spritecollide(
            self.player,
            self.platforms,
            dokill=False
        )
        # check if player hits a platform - only going downward
        if self.player.velocity.y > 0:
            if hits:
                self.player.position.y = hits[0].rect.top + 1
                self.player.velocity.y = 0

    def events(self):
        ''' manage events/interactions with users '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def update(self):
        ''' update screen after drawing and checking events '''
        self.all_sprites.update()
        self._detect_collisions()

    def show_title(self):
        pass

    def show_gameover(self):
        pass

    def _load_gfx(self):
        ''' Load all game graphics '''
        # self.background = pg.image.load(
        #    os.path.join(IMG_PATH, 'Background/space_background.png')
        # ).convert()
        # self.background_rect = self.background.get_rect()
        pass

    def _load_snd(self):
        # Load all sounds
        #self.laser_snd = pg.mixer.Sound(
        #    os.path.join(SND_PATH, 'laser.wav')
        #)
        # Load background music
        #pg.mixer.music.load(
        #    os.path.join(SND_PATH, 'background.ogg')
        #)
        #pg.mixer.music.set_volume(0.4)
        pass

    @staticmethod
    def draw_text(surface, text, size, pos):
        # font = pg.font.Font(FONT_NAME, size)
        font = pg.font.Font(None, size)
        text_surface = font.render(text, True, rgb('white'))
        text_rect = text_surface.get_rect()
        x, y = pos
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)


if __name__ == "__main__":
    pyu = Game()
    pyu.show_title()

    while pyu.running:
        pyu.new()
        pyu.show_gameover()

    pg.quit()
    sys.exit(0)

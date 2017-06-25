#!/usr/bin/env python3
''' Pyu, a simple platformer game made in Pygame

Inspired by the wonderful KidsCanCode videos on youtube
'''
import sys
import pygame as pg
import random
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
        self.score = 0
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
            # Player is off screen. Then more sprites on screen after
            # the scroll_window_down anim
            if self.player.rect.bottom > HEIGHT:
                # scroll down a bit before dying
                self._scroll_window_down()
            if len(self.platforms) == 0:
                self.playing = False

    def draw(self):
        ''' draw objects on screen '''
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)

        Game.draw_text(
            self.screen,
            "Score = {}".format(self.score),
            20,
            (WIDTH / 2, 10)
        )
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
            "collide = {}".format(
                len(pg.sprite.spritecollide(
                    self.player,
                    self.platforms,
                    False))
            ),
            20,
            (90, 70)
        )

        Game.draw_text(
            self.screen,
            "Player = ({}, {})".format(
                round(self.player.position.x),
                round(self.player.position.y)
            ),
            20,
            (90, 90)
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

    def _scroll_window_down(self):
        ''' move all sprites down until there is no sprite left '''
        for sprite in self.all_sprites:
            sprite.rect.y -= max(self.player.velocity.y, 10)
            if sprite.rect.bottom <= 0:
                sprite.kill()

    def _scroll_window_up(self):
        ''' return true if we have to scroll the window up
        That happens if the player reaches a certain height '''
        res = False
        if self.player.rect.top < HEIGHT / 4:
            res = True
            self.player.position.y += abs(self.player.velocity.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.velocity.y)
                # kill the platforms that went below a certain point
                # to keep the size of self.platforms small enough
                # Also, that gives us points !
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 1
        return res

    def _spawn_new_platforms(self, n):
        ''' randomly spawn n new platforms on screen, above HEIGHT / 4 '''
        while len(self.platforms) <= n:
            width = random.randrange(50, 100)
            x = random.randrange(0, WIDTH - width)
            y = random.randrange(-75, 30)
            p = Platform(x, y, width, 20)
            self.all_sprites.add(p)
            self.platforms.add(p)

    def events(self):
        ''' manage events/interactions with users '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = self.playing = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def update(self):
        ''' update screen after drawing and checking events '''
        self.all_sprites.update()
        self._detect_collisions()
        if self._scroll_window_up():
            self._spawn_new_platforms(12)

    def show_title(self):
        self.screen.fill(BGCOLOR)
        Game.draw_text(self.screen, "Pyu", 80, (WIDTH / 2, HEIGHT / 2))
        Game.draw_text(self.screen,
                       "Use Space bar to jump",
                       40,
                       (WIDTH / 2, HEIGHT / 2 + 100))
        Game.draw_text(self.screen,
                       "Press any key to continue...",
                       20, (WIDTH / 2, HEIGHT - 20))
        pg.display.flip()
        self._wait_keypress()

    def show_gameover(self):
        # don't show it if we wanted force quit
        if not self.running:
            return

        self.screen.fill(BGCOLOR)
        Game.draw_text(self.screen, "Game Over", 80, (WIDTH / 2, HEIGHT / 2))
        Game.draw_text(self.screen,
                       "Score = {}".format(self.score),
                       40, (WIDTH / 2, HEIGHT / 2 + 100))
        Game.draw_text(self.screen,
                       "Press any key to continue...",
                       20, (WIDTH / 2, HEIGHT - 20))
        pg.display.flip()
        self._wait_keypress()

    def _wait_keypress(self):
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    waiting = False

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

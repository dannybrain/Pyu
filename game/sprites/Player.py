import pygame as pg

from settings import *

# redefine/shorten vector definition
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        # character's state
        self.walking = False
        self.jumping = False
        # load character initial image
        self._load_images(game)
        # load animation frames
        self._load_frames(game)

    def _load_images(self, game):
        self.image = game.spritesheet.get_image(
            x=690,
            y=406,
            width=120,
            height=201
        )
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

    def _load_frames(self, game):
        # current animation frame
        self.frame = 0
        self.last_update = 0
        self.standing_frames = [
            game.spritesheet.get_image(690, 406, 120, 201),
            game.spritesheet.get_image(614, 1063, 120, 191)
        ]
        for img in self.standing_frames:
            img.set_colorkey(BLACK)

        self.walking_frames_r = [
            game.spritesheet.get_image(678, 860, 120, 201),
            game.spritesheet.get_image(692, 1458, 120, 207)
        ]
        self.walking_frames_l = []
        for img in self.walking_frames_r:
            img.set_colorkey(BLACK)
            self.walking_frames_l.append(
                pg.transform.flip(img, True, False)
            )

        self.jump_frame = game.spritesheet.get_image(382, 763, 150, 181)
        self.jump_frame.set_colorkey(BLACK)

    def _animate(self):
        now = pg.time.get_ticks()
        # determine character's state
        self.walking = True if (self.velocity.x != 0) else False

        # change frame animation based on state
        if self.walking:
            if now - self.last_update > WALKING_ANIMATION_SPEED:
                self.last_update = now
                # save image rectangle
                bottom = self.rect.bottom
                self.frame = (self.frame + 1) % len(self.walking_frames_r)
                # walking toward right
                if self.velocity.x > 0:
                    self.image = self.walking_frames_r[self.frame]
                else:
                    self.image = self.walking_frames_l[self.frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.walking and not self.jumping:
            if now - self.last_update > IDLE_ANIMATION_SPEED:
                self.last_update = now
                # save image rectangle
                bottom = self.rect.bottom
                self.frame = (self.frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.frame]
                # restore image position to keep it centered
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    def jump_cut(self):
        ''' stop the jump by reducing the player velocity '''
        if self.jumping:
            if self.velocity.y < PLAYER_JMP_CUT:
                self.velocity.y = PLAYER_JMP_CUT

    def jump(self):
        # jump only if staying on top of a platform
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.velocity.y = PLAYER_JMP_FORCE
            self.jumping = True
            self.game.jump_snd.play()

    def update(self):
        self.acceleration = vec(0, PLAYER_GRAVITY)
        # animate character based on its stat()
        self._animate()

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
        # if velocity is really low, reset to 0 to avoid confusion when
        # testing character's state
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0

        # check edges
        if self.position.x > (WIDTH + self.rect.width / 2):
            self.position.x = 0
        elif self.position.x + self.rect.width / 2 <= 0:
            self.position.x = WIDTH - self.rect.width / 2

        self.rect.midbottom = self.position

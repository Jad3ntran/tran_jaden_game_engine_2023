import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
from pygame.math import Vector2 as vec
import os
from settings import *
from settings import *
from math import floor

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - cooldown reset
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'ninja.png')).convert()
        self.image.set_colorkey(WHITE)
        self.health = 150
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0) 
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if hits:
            print("i can jump")
            if self.rect.bottom >= hits[0].rect.top - 1:
                self.vel.y = -PLAYER_JUMP
    def update(self):
        # Check for collisions with platforms
        phits = pg.sprite.spritecollide(self, self.game.all_platforms, False)
        if self.vel[0] >= 0 and phits:
            if self.rect.right < phits[0].rect.left + 35:
                print("i just hit the left side of a box...")
                self.vel[0] = 0 # stop horizontal movement
                self.pos.x = phits[0].rect.left - 35
        # Gravity and controls
        self.acc = vec(0, PLAYER_GRAV)
        self.controls()
        self.acc.x += self.vel.x * -PLAYER_FRIC
        # Equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # Prevent going off the left side of the screen
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        # Update player position
        self.rect.midbottom = self.pos
        # Check for collisions with mobs and when the collisions occur
        mhits = pg.sprite.spritecollide(self, self.game.all_mobs, True)
        if mhits:
            # when player hits mob, health is decreased by 10
            self.health -= 10




# platforms

class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        # Constructor for the Platform class, initializes its properties
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(MIDNIGHTBLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 5
    def update(self):
        # Method to update the platform's position, especially if it's a moving platform
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed

class Mob(Sprite):
    def __init__(self, game, x, y, w, h, kind):
        # Constructor for the Mob class, initializes its properties
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        # Load the image for the mob (drone.png) and set the color key
        self.image = pg.image.load(os.path.join(img_folder, "drone.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(WIDTH/2, HEIGHT/2)
    # causes "mobs" to seek the player (moving left when player moves left, moving right when player moves right, etc.)
    def seeking(self):
        if self.rect.x < self.game.player.rect.x:
            self.rect.x += 2
        if self.rect.x > self.game.player.rect.x:
            self.rect.x -= 2
        if self.rect.y < self.game.player.rect.y:
            self.rect.y += 2
        if self.rect.y > self.game.player.rect.y:
            self.rect.y -= 2
    def spawn(self):
        # Method to randomly spawn a mob within the screen boundaries
        self.rect.x = randint(0, WIDTH)
        self.rect.y = randint(0, HEIGHT/2)
    def update(self):
            # Method to update the mob's behavior, in this case, seeking the player
            self.seeking()

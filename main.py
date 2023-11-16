# This file was created by Jaden Tran

# Code from Chris Bradfield tutorials content from kids can code: http://kidscancode.org/blog/
# https://github.com/kidscancode/pygame_tutorials/tree/master/platform 
# https://opensource.com/article/18/7/put-platforms-python-game
# https://www.chegg.com/homework-help/questions-and-answers/python-pygame-basic-template-player-green-rectangle-enemies-spawn-want-enemies-keep-spawni-q34176873

# GameDesign:
'''
Goals: survive as long as you can
Rules: don't touch mobs
Feedback: score on top of the screen, score based on the time of survival 
Freedom Run side to side, jump
'''

'''
Feature Goals: 
- new mobs spawn in every few seconds (harder the longer you survive
- game says gameover when player dies
'''

# Importing necessary libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import os
from settings import *
from sprites import *

vec = pg.math.Vector2

# Setup asset folders for images and sounds
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')

class Game:
    def __init__(self):
        # Initialize pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
        self.paused = False
        self.cd = Cooldown()
        self.start_time = pg.time.get_ticks()
        self.mob_spawn_cd = Cooldown()
        self.mob_spawn_interval = 1  # Adjust the interval as needed
        self.last_mob_spawn_time = 0
        self.game_over = False

    def new(self):
        # Create a group for all sprites
        self.bgimage = pg.image.load(os.path.join(img_folder, "cb277.png")).convert()
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.all_platforms = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        # Instantiate classes
        self.player = Player(self)
        # Add instances to groups
        self.all_sprites.add(self.player)
        self.mob_spawn_cd.event_reset()
        self.last_mob_spawn_time = pg.time.get_ticks() // 1000

        for p in PLATFORM_LIST:
            # Instantiate the Platform class
            plat = Platform(*p)
            self.all_sprites.add(plat)
            self.all_platforms.add(plat)

        # Create mobs (15)
        for m in range(0, 15):
            m = Mob(self, randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "normal")
            self.all_sprites.add(m)
            self.all_mobs.add(m)

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if not self.game_over:
            self.all_sprites.update()
            # if player health hits 0 or if player falls off of the screen, game ends
            if self.player.health <= 0 or self.player.rect.top > HEIGHT:
                self.game_over = True
                # stop updating the score when the game is over
                self.cd.delta = pg.time.get_ticks() // 1000 - self.start_time // 1000
            else:
                elapsed_time = pg.time.get_ticks() - self.start_time
                self.cd.delta = elapsed_time // 1000  # Convert milliseconds to seconds

        # Prevent the player from falling through the platform
        hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
        if hits:
            if self.player.vel.y > 0:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                print(self.player.vel.y)
                print(self.player.acc.y)
            elif self.player.vel.y < 0:
                self.player.vel.y = -self.player.vel.y

        # Check if it's time to spawn a new mob
        current_time = pg.time.get_ticks() // 1000
        if current_time - self.last_mob_spawn_time >= self.mob_spawn_interval:
            self.spawn_new_mob()
            self.last_mob_spawn_time = current_time

        # Prevent the player from jumping up through a platform
        if self.player.vel.y < 0:
            hits = pg.sprite.spritecollide(self.player, self.all_platforms, False)
            if hits:
                if self.player.rect.bottom >= hits[0].rect.top - 1:
                    self.player.rect.top = hits[0].rect.bottom
                    self.player.acc.y = 5
                    self.player.vel.y = 0
            hits = pg.sprite.spritecollide(self.player, self.all_mobs, False)
            if hits:
                print("ouch")

    def spawn_new_mob(self):
        # Method to spawn a new mob at a random position
        new_mob = Mob(self, randint(0, WIDTH), randint(0, HEIGHT/2), 20, 20, "normal")
        # Add the new mob to both the all_sprites and all_mobs groups
        self.all_sprites.add(new_mob)
        self.all_mobs.add(new_mob)

    def events(self):
        # Method to handle events, such as quitting the game or detecting key releases
        print("Checking for events")
        for event in pg.event.get():
            # Check for a closed window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.running = False
                    print("Key up event detected")

    def draw(self):
        # Draw the background screen
        if not self.game_over:
            self.screen.fill(CHOCO)
            self.screen.blit(self.bgimage, (0, 0))
            # Draw all sprites
            self.all_sprites.draw(self.screen)
            # if self.player.health <= 0:
            #     self.draw_text("Game Over", 48, WHITE, WIDTH / 2, HEIGHT / 4)
            self.draw_text("Score: " + str(self.cd.delta), 22, WHITE, WIDTH/2, HEIGHT/10)
            self.draw_text("Health:" + str(self.player.health), 22, WHITE, WIDTH/2, HEIGHT/24)
            # Buffer - after drawing everything, flip the display
            pg.display.flip()
        else:
            print("something")
            self.screen.fill(BLACK)
            self.draw_text("Game Over", 48, WHITE, WIDTH / 2, HEIGHT / 4)
            self.draw_text("Your Score: " + str(self.cd.delta), 32, WHITE, WIDTH / 2, HEIGHT / 2)
            pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
    
    def show_go_screen(self):
        print("show go screen method called")
        self.screen.fill(BLACK)
        self.draw_text("Game Over", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Your Score: " + str(self.cd.delta), 32, WHITE, WIDTH / 2, HEIGHT / 2)
        pg.display.flip

g = Game()
while g.running:
    g.new()

pg.quit()
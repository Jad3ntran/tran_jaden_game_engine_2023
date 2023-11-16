# This file was created by: Jaden Tran
# Content from Chris Bradfield; Kids Can Code
# KidsCanCode - Game Development with Pygame video series
# Video link: https://youtu.be/OmlQ0XCvIn0 

# game settings 
WIDTH = 1024
HEIGHT = 768
FPS = 30

# player settings
PLAYER_JUMP = 30
PLAYER_GRAV = 1.5
global PLAYER_FRIC
PLAYER_FRIC = 0.2

# Define colors using RGB values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SAND = (238,213,183)
BURNTSIENNA = (138,54,15)
BROWN4 = (139,35,35)
CHOCO = (255,127,36)
DARKVIOLET = (148,50,211)
GRAY = (54,54,54)
MIDNIGHTBLUE = (25,25,112)

# List of platforms with their positions, dimensions, and categories
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40, "normal"),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20,"normal"),
                 (125, HEIGHT - 350, 100, 20, "moving"),
                 (150, 200, 100, 20, "normal"),
                 (425, 100, 200, 20, "normal"),
                 (100, 500, 150, 20, "normal"),
                 (200, 300, 200, 20, "normal"),
                 (700, 400, 100, 20, "moving"), 
                 (600, 250, 150, 20, "normal"),
                 (500, 180, 100, 20, "normal"),
                 (650, 600, 150, 20, "normal"),
                 (50, 350, 150, 20, "normal")]
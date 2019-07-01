# Copyright © 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Example code, drawn from
# https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap

import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARKBLUE = (0, 0, 50)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 120
TITLE = "Undervoid"
BGCOLOR = DARKBLUE

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

CURSOR_IMG = 'cursor.gif'
WALL_IMG = 'voidwall.png'
FLOOR_IMG = 'dungeonfloor.png'
ICON_IMG = 'voidbullet.png'

THEME_1 = 'Leaving Home.mp3'

# player settings
PLAYER_SPEED = 500
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'voidwalker.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

# mob settings
THRALL_IMG = 'thrall.png'
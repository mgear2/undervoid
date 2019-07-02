# Copyright © 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Building off example code from
# https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap

import pygame as pg
vec = pg.math.Vector2

""" General Settings: COLORS, GEN_SETTINGS, GRID_SETTINGS
"""
COLORS = {
    'WHITE': (255, 255, 255), # (R, G, B)
    'BLACK': (0, 0, 0),
    'DARKGREY': (40, 40, 40),
    'LIGHTGREY': (100, 100, 100),
    'GREEN': (0, 255, 0),
    'RED': (255, 0, 0),
    'YELLOW': (255, 255, 0),
    'DARKBLUE':  (0, 0, 50)
}

GEN_SETTINGS = {
    'WIDTH': 1024,   # 16 * 64 or 32 * 32 or 64 * 16
    'HEIGHT': 768,  # 16 * 48 or 32 * 24 or 64 * 12
    'FPS': 120,
    'TITLE': 'Undervoid',
    'BGCOLOR': COLORS['DARKBLUE'],
    'TILESIZE': 64,
}

GRID_SETTINGS = {
    'GRIDWIDTH': GEN_SETTINGS['WIDTH'] / GEN_SETTINGS['TILESIZE'],
    'GRIDHEIGHT': GEN_SETTINGS['HEIGHT'] / GEN_SETTINGS['TILESIZE'],
}

""" Entity Settings: PLAYER_SETTINGS, WEAPON_SETTINGS, MOB_SETTINGS
"""
PLAYER_SETTINGS = {
    'SPEED': 500,
    'ROT_SPEED': 250,
    'HIT_RECT': pg.Rect(0, 0, 35, 35),
    'HAND_OFFSET': vec(35, 30)
}

WEAPON_SETTINGS = {
    'VBULLET_SPEED': 1000,
    'VBULLET_LIFETIME': 1000,
    'VBULLET_RATE': 150,
    'VSPREAD': 5
}

MOB_SETTINGS = {
    'THRALL_SPEED': 250,
    'THRALL_HIT_RECT': pg.Rect(0, 0, 35, 35)
}

""" Media: IMAGES, MUSIC, SOUND
"""
IMAGES = {
    'TITLE_IMG': 'undervoidtitle.png',
    'PLAYER_IMG': 'voidwalker.png',
    'CURSOR_IMG': 'cursor.gif',
    'WALL_IMG': 'voidwall.png',
    'FLOOR_IMG': 'dungeonfloor.png',
    'ICON_IMG': 'voidbullet.png',
    'THRALL_IMG': 'thrall.png',
    'VBULLET_IMG': 'voidbullet.png'
}

MUSIC = {
    'leavinghome': 'Leaving Home.mp3',
    'voidwalk': 'voidwalk.wav'
}

SOUNDS = {}
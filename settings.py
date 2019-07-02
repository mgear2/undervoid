# Copyright (c) 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Building off example code from
# https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap

import pygame as pg
vec = pg.math.Vector2

""" General Settings: COLORS, GEN, GRID
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

GEN = {
    'WIDTH': 1024,   # 16 * 64 or 32 * 32 or 64 * 16
    'HEIGHT': 768,  # 16 * 48 or 32 * 24 or 64 * 12
    'FPS': 120,
    'TITLE': 'Undervoid',
    'BGCOLOR': COLORS['BLACK'],
    'TILESIZE': 64,
}

GRID = {
    'GRIDWIDTH': GEN['WIDTH'] / GEN['TILESIZE'],
    'GRIDHEIGHT': GEN['HEIGHT'] / GEN['TILESIZE'],
}

""" Entity Settings: PLAYER, WEAPON, MOB
"""
PLAYER = {
    'SPEED': 600,
    'ROT_SPEED': 250,
    'HIT_RECT': pg.Rect(0, 0, 35, 35),
    'HAND_OFFSET': vec(35, 30),
    'DMG_MULT': 1.0,
    'HP': 100
}

WEAPON = {
    'VBULLET_SPEED': 1500 + PLAYER['SPEED'],
    'VBULLET_LIFETIME': 1000,
    'VBULLET_RATE': 150,
    'VSPREAD': 5,
    'VDMG': 10 * PLAYER['DMG_MULT']
}

MOB = {
    'THRALL_SPEED': 750,
    'THRALL_HIT_RECT': pg.Rect(0, 0, 35, 35),
    'THRALL_HP': 1,
    'THRALL_DMG': 10,
    'THRALL_KB': 20 # knockback
}

""" Media: IMG, MUSIC, SOUND
"""
IMG = {
    'TITLE_IMG': 'undervoidtitle.png',
    'PLAYER_IMG': 'voidwalker.png',
    'CURSOR_IMG': 'cursor.gif',
    'WALL_IMG': 'voidwall.png',
    'FLOOR_IMG_1': 'dungeonfloor01.png',
    'FLOOR_IMG_2': 'dungeonfloor02.png',
    'FLOOR_IMG_3': 'dungeonfloor03.png',
    'FLOOR_IMG_4': 'dungeonfloor04.png',
    'FLOOR_IMG_5': 'dungeonfloor05.png',
    'FLOOR_IMG_6': 'dungeonfloor06.png',
    'ICON_IMG': 'voidbullet.png',
    'THRALL_IMG': 'thrall.png',
    'VBULLET_IMG': 'voidbullet.png',
    'SKULL': 'skull01.png'
}

MUSIC = {
    'leavinghome': 'Leaving Home.mp3',
    'voidwalk': 'voidwalk.wav'
}

SOUNDS = {}
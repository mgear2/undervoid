# Copyright (c) 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Building off example code from
# https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap

""" General Settings: COLORS, GEN, GRID, LAYER
"""
COLORS = {
    "WHITE": (255, 255, 255),  # (R, G, B)
    "BLACK": (0, 0, 0),
    "DARKGREY": (40, 40, 40),
    "LIGHTGREY": (100, 100, 100),
    "GREEN": (0, 255, 0),
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "DARKBLUE": (0, 0, 50),
    "MEDIUMVIOLETRED": (199, 21, 133, 255),
}

# https://fschutt.github.io/pygame3-colors/
VOID_COLORS = [
    "black",
    "gray0",
    "gray1",
    "darkmagenta",
    "darkviolet",
    "purple4",
    "mediumvioletred",
    "deepskyblue4",
]

GEN = {
    "SCREEN": "win",
    "WIDTH": 1440,
    "HEIGHT": 900,
    "FPS": 60,
    "TITLE": "Undervoid",
    "TILESIZE": 64,
    "TITLE_DIMENSIONS": (535, 65),
}

LAYER = {
    "FLOOR": 0,
    "GRAVE": 0,
    "WALL": 1,
    "ITEM": 1,
    "PLAYER_MOVE": 1,
    "PLAYER": 2,
    "MOB": 2,
    "BULLET": 3,
    "VFX": 4,
    "CURSOR": 5,
}

""" Entity Settings: PLAYER, WEAPON, MOB, ITEMS
"""
PLAYER = {
    "SIZE": GEN["TILESIZE"] * 2,
    "SPEED": GEN["TILESIZE"] * 8,
    "ROT_SPEED": 250,
    "HIT_RECT": (0, 0, 35, 35),
    "HAND_OFFSET": (65, 25),
    "DMG_MULT": 1.5,
    "HP": 100,
}

WEAPON = {
    "VBULLET_SPEED": 1500 + PLAYER["SPEED"],
    "VBULLET_LIFETIME": GEN["TILESIZE"] * 10,
    "VBULLET_RATE": 150,
    "VSPREAD": 5,
    "VDMG": 10 * PLAYER["DMG_MULT"],
    "VBULLET_VFX": [
        "voiddust01.png",
        "voiddust02.png",
        "voiddust03.png",
        "voiddust04.png",
    ],
    "VDUST_SIZE": GEN["TILESIZE"],
    "VDUST_LIFETIME": 40,
}

MOB = {
    "THRALL_SPEED": [10, 11, 12, 13],  # [600, 650, 700, 750],
    "THRALL_HIT_RECT": (0, 0, GEN["TILESIZE"] / 2, GEN["TILESIZE"] / 2),
    "THRALL_HP": 75,
    "THRALL_DMG": 15,
    "THRALL_KB": 20,  # knockback
    "THRALL_RADIUS": GEN["TILESIZE"],
    "DETECT_RADIUS": GEN["TILESIZE"] * 12,
    "DROP_CHANCE": 0.35,
    "DMG_RATE": 150,
}

ITEMS = {"POTION_1_HP": 0.20 * PLAYER["HP"], "BOB_RANGE": 15, "BOB_SPEED": 0.4}

""" Media: IMG, MUSIC, SOUNDS
"""
IMG = {
    "TITLE": "undervoidtitle.png",
    "VOIDWALKER": ["voidwalker_magic.png", "voidwalker_coachgun.png"],
    "VOIDWALKER_MOVE": [
        "voidwalkermove01.png",
        "voidwalkermove02.png",
        "voidwalkermove01.png",
        "voidwalkermove03.png",
        "voidwalkermove04.png",
        "voidwalkermove03.png",
    ],
    "CURSOR": [
        "cursor01.png",
        "cursor02.png",
        "cursor03.png",
        "cursor03.png",
        "cursor02.png",
        "cursor01.png",
    ],
    "VOIDWALL": "voidwall.png",
    "D_FLOOR": [
        "dungeonfloor01.png",
        "dungeonfloor02.png",
        "dungeonfloor03.png",
        "dungeonfloor04.png",
        "dungeonfloor05.png",
    ],
    "ICON": "undervoidicon.png",
    "THRALL": "thrall.png",
    "VBULLET": "voidbullet02.png",
    "SKULL": "skull01.png",
    "THRALL_GRAVE": ["thrallgrave01.png", "thrallgrave02.png", "thrallgrave03.png"],
    "POTION_1": "potion01.png",
}

MUSIC = {"leavinghome": "Leaving Home.mp3", "voidwalk": "voidwalk.wav"}

SOUNDS = {
    "growl01": "growl01.wav",
    "treasure01": "treasure01.wav",
    "treasure02": "treasure02.wav",
    "woadbear01": "woadbear01.wav",
    "wave01": "wave01.wav",
    "hit01": "hit01.wav",
    "hit02": "hit02.wav",
    "hit03": "hit03.wav",
}

HIT_SOUNDS = ["hit01", "hit02", "hit03"]

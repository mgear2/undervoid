# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg


class Grouping:
    def __init__(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.pmove_sprite = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.stops_bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.graves = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        self.cursor_sprite = pg.sprite.Group()
        self.weaponvfx_sprite = pg.sprite.Group()
        self.spawners = pg.sprite.Group()

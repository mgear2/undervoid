# Copyright (c) 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Building off example code from
# https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap

import pygame as pg
from settings import *
from random import choice
from os import sys

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, game, filename):
        self.data = []
        self.game = game
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip('\n'))
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * GEN['TILESIZE']
        self.height = self.tileheight * GEN['TILESIZE']

    def render(self, surface):
        for row, tiles in enumerate(self.data):
            row *= GEN['TILESIZE']
            for col, tile in enumerate(tiles):
                col *= GEN['TILESIZE']
                if tile != ' ' and tile != '0':
                    self.floor_img = choice(self.game.floor_img)
                    surface.blit(self.floor_img, (col, row))
                if tile == '1':
                    surface.blit(self.game.wall_img, (col, row))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height, cursor):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.cursor = cursor

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(GEN['WIDTH'] / 2)
        y = -target.rect.centery + int(GEN['HEIGHT'] / 2)
        self.camera = pg.Rect(x, y, self.width, self.height)
        self.cursor.rect.centerx -= x
        self.cursor.rect.centery -= y
        self.cursor.pos = self.cursor.rect.center
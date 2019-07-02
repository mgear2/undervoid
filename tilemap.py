# Copyright © 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Building off example code from
# https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap

import pygame as pg
from settings import *
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
        self.width = self.tilewidth * GEN_SETTINGS['TILESIZE']
        self.height = self.tileheight * GEN_SETTINGS['TILESIZE']
        self.floor_img = game.floor_img

    def render(self, surface):
        x = 0
        while x < self.width:
            y = 0
            while y < self.height:
                surface.blit(self.floor_img, (x, y))
                y += GEN_SETTINGS['TILESIZE']
            x += GEN_SETTINGS['TILESIZE']

        """for x in range(0, self.width):
            for y in range(0, self.height):
                surface.blit(self.floor_img, (x * GEN_SETTINGS['TILESIZE'],
                                     y * GEN_SETTINGS['TILESIZE']))"""

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(GEN_SETTINGS['WIDTH'] / 2)
        y = -target.rect.centery + int(GEN_SETTINGS['HEIGHT'] / 2)
        self.camera = pg.Rect(x, y, self.width, self.height)
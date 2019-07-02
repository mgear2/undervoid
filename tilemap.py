# Copyright © 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Building off example code from
# https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap

import pygame as pg
from settings import *

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip('\n'))

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * GEN_SETTINGS['TILESIZE']
        self.height = self.tileheight * GEN_SETTINGS['TILESIZE']

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(GEN_SETTINGS['WIDTH'] / 2)
        y = -target.rect.centery + int(GEN_SETTINGS['HEIGHT'] / 2)
        self.camera = pg.Rect(x, y, self.width, self.height)
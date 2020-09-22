# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg


class Camera:
    """
    Camera class is used to center the game window on the player
    and move the map and contained entities relative to the player.
    """

    def __init__(self, game, width, height, cursor):
        self.game = game
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.cursor = cursor

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.game.settings["gen"]["width"] / 2)
        y = -target.rect.centery + int(self.game.settings["gen"]["height"] / 2)
        self.camera = pg.Rect(x, y, self.width, self.height)
        self.cursor.rect.centerx -= x
        self.cursor.rect.centery -= y
        self.cursor.pos = self.cursor.rect.center

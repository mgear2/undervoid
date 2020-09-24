# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml

class Camera:
    """
    Camera class is used to center the game window on the player
    and move the map and contained entities relative to the player.
    """

    def __init__(self, settings: ruamel.yaml.comments.CommentedMap, width: int, height: int, cursor: pg.sprite.Sprite):
        self.settings = settings
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.cursor = cursor

    def apply(self, entity: pg.sprite.Sprite):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect: pg.Rect):
        return rect.move(self.camera.topleft)

    def update(self, target: pg.sprite.Sprite):
        x = -target.rect.centerx + int(self.settings["gen"]["width"] / 2)
        y = -target.rect.centery + int(self.settings["gen"]["height"] / 2)
        self.camera = pg.Rect(x, y, self.width, self.height)
        self.cursor.rect.centerx -= x
        self.cursor.rect.centery -= y
        self.cursor.pos = self.cursor.rect.center

# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml


class Cursor(pg.sprite.Sprite):
    """
    Cursor class provides an animated cursor target image to
    replace the default cursor.
    """

    def __init__(
        self,
        settings: ruamel.yaml.comments.CommentedMap,
        sprite_groups: (pg.sprite.Group),
        cursor_img: list,
    ):
        self._layer = settings["layer"]["cursor"]
        self.groups = sprite_groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.cursor_img = cursor_img
        self.image = cursor_img[0]
        self.rect = self.image.get_rect()
        self.rect.center = pg.mouse.get_pos()
        self.pos = pg.mouse.get_pos()
        self.counter = 0
        self.last = 0

    def update(self):
        now = pg.time.get_ticks()
        if now > self.last + 100:
            self.counter += 1
            self.last = now
        if self.counter > 5:
            self.counter = 0
        self.image = self.cursor_img[self.counter]
        self.rect.center = pg.mouse.get_pos()
        self.pos = pg.mouse.get_pos()

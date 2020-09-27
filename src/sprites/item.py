# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml
import pytweening as tween

vec = pg.math.Vector2


class Item(pg.sprite.Sprite):
    """
    Item class is used to place items on the map.
    Items use tween animations from the pytweening library.
    """

    def __init__(
        self,
        settings: ruamel.yaml.comments.CommentedMap,
        sprite_groups: (pg.sprite.Group),
        game_client_data_item_img: pg.Surface,
        pos: vec,
        img,
        kind: str,
    ):
        self.settings = settings
        self._layer = self.settings["layer"]["item"]
        self.bob_range = self.settings["items"]["bob_range"]
        self.bob_speed = self.settings["items"]["bob_speed"]
        self.groups = sprite_groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game_client_data_item_img[img]
        self.kind = kind
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # item bobbing motion
        offset = self.bob_range * (self.tween(self.step / self.bob_range) - 0.5)
        self.rect.centery = self.pos[1] + offset * self.dir
        self.step += self.bob_speed
        if self.step > self.bob_range:
            self.step = 0
            self.dir *= -1

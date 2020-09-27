# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml
from src.sprites.grouping import Grouping

vec = pg.math.Vector2


class Legs(pg.sprite.Sprite):
    """
    Sprite for player movement is currently separate from the player.
    Legs must be initialized in the same location as the player; layering
    ensures it is rendered underneath the player.
    Updating Legs cycles the image, providing an animation effect as the player walks.
    """

    def __init__(
        self,
        settings: ruamel.yaml.comments.CommentedMap,
        sprite_groups: (pg.sprite.Group),
        player_img: pg.Surface,
        x=0,
        y=0,
    ):
        self._layer = settings["layer"]["player_move"]
        pg.sprite.Sprite.__init__(self, sprite_groups)
        self.images = player_img
        self.image = self.images[0]
        self.current = self.image
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.pos = vec(x, y) * settings["gen"]["tilesize"]
        self.rot = 0
        self.last = 0
        self.i = 0

    def place(self, x, y: int):
        self.pos = vec(x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, velocity: [int], player_position: vec):
        now = pg.time.get_ticks()
        if velocity != [0, 0]:
            self.rot = (velocity).angle_to(vec(1, 0)) % 360
            if now - self.last > 100:
                self.last = now
                self.current = self.images[self.i]
                self.i += 1
                if self.i >= len(self.images):
                    self.i = 0
        self.image = pg.transform.rotate(self.current, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = player_position

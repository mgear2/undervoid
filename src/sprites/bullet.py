# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml
from src.sprites.grouping import Grouping
from random import uniform

vec = pg.math.Vector2


class Bullet(pg.sprite.Sprite):
    """
    Bullet class provides bullet sprites with image, velocity and lifetime tracking.
    """

    def __init__(
        self,
        settings: ruamel.yaml.comments.CommentedMap,
        sprite_grouping: Grouping,
        game_client_data_vbullet_img: pg.Surface,
        pos: vec,
        dir: vec,
        rot: float,
    ):
        self.settings = settings
        self._layer = self.settings["layer"]["bullet"]
        self.sprite_grouping = sprite_grouping
        self.groups = sprite_grouping.all_sprites, sprite_grouping.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rot = rot
        self.image = pg.transform.rotate(game_client_data_vbullet_img, self.rot + 90)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(
            -self.settings["weapon"]["vbullet"]["spread"],
            self.settings["weapon"]["vbullet"]["spread"],
        )
        self.vel = dir.rotate(spread) * self.settings["weapon"]["vbullet"]["speed"]
        self.spawn_time = pg.time.get_ticks()

    def update(self, game_client_dt: float):
        self.pos += self.vel * game_client_dt
        self.rect.center = self.pos
        if (
            pg.sprite.spritecollideany(self, self.sprite_grouping.stops_bullets)
            or pg.time.get_ticks() - self.spawn_time
            > self.settings["weapon"]["vbullet"]["life"]
        ):
            self.kill()

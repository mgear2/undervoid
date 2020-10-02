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
        game_client_data_vbullet_img: pg.Surface,
        pos: vec,
        direction: vec,
        rot: float,
    ):
        self.settings, self.rot = settings, rot
        self._layer = self.settings["layer"]["bullet"]
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.rotate(game_client_data_vbullet_img, self.rot + 90)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(
            -self.settings["weapon"]["vbullet"]["spread"],
            self.settings["weapon"]["vbullet"]["spread"],
        )
        self.lifetime = self.settings["weapon"]["vbullet"]["life"]
        self.vel = (
            direction.rotate(spread) * self.settings["weapon"]["vbullet"]["speed"]
        )
        self.spawn_time = pg.time.get_ticks()

    def update(self, game_client_dt: float, bullets, stops_bullets: pg.sprite.Group):
        self.pos += self.vel * game_client_dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
        pg.sprite.groupcollide(bullets, stops_bullets, True, False)

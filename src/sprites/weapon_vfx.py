# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml
from random import choice

vec = pg.math.Vector2


class Weapon_VFX(pg.sprite.Sprite):
    """
    Weapon_VFX appear when the player is shooting.
    Cycling between available img options provides
    animation effect.
    """

    def __init__(
        self,
        settings: ruamel.yaml.comments.CommentedMap,
        sprite_groups: (pg.sprite.Group),
        game_client_data_weaponvfx: list,
        pos: vec,
    ):
        self.settings = settings
        self._layer = self.settings["layer"]["vfx"]
        self.groups = sprite_groups
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = pg.transform.scale(
            choice(game_client_data_weaponvfx),
            (
                self.settings["gen"]["tilesize"],
                self.settings["gen"]["tilesize"],
            ),
        )
        self.rect = self.image.get_rect()
        self.pos = self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if (
            pg.time.get_ticks() - self.spawn_time
            > self.settings["weapon"]["vbullet"]["fx_life"]
        ):
            self.kill()

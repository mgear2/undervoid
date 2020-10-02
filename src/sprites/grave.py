# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml
from random import choice

vec = pg.math.Vector2


class Grave(pg.sprite.Sprite):
    """
    Graves are left behind when mobs are killed,
    with rotation matched to the mob rotation on death.
    Grave images are a random choice from graves available
    for that enemy kind.
    """

    def __init__(
        self,
        settings: ruamel.yaml.comments.CommentedMap,
        game_client_data_mob_img: pg.Surface,
        kind: str,
        pos: vec,
        rot: float,
    ):
        self.settings = settings
        self._layer = self.settings["layer"]["grave"]
        pg.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = pg.transform.rotate(
            pg.transform.scale(
                choice(game_client_data_mob_img["grave"][kind]),
                (
                    self.settings["gen"]["tilesize"],
                    self.settings["gen"]["tilesize"],
                ),
            ),
            rot,
        )
        self.rect = self.image.get_rect()
        self.rect.center = pos

# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml
from random import randint, random
from src.sprites.mob import Mob
from src.sprites.player import Player
from src.sprites.grouping import Grouping

vec = pg.math.Vector2


class Spawner(pg.sprite.Sprite):
    """
    Spawner objects are placed on the map; when the player is within a certain distance,
    and if there are not already too many mobs present, the spawner will spawn mobs.
    """

    def __init__(
        self,
        settings: ruamel.yaml.comments.CommentedMap,
        level_data,
        img: list,
        col,
        row: int,
    ):
        self.level_data = level_data
        self.img = img
        self.settings = settings
        pg.sprite.Sprite.__init__(self)
        self.cols, self.rows = col, row
        self.pos = vec(col, row) * settings["gen"]["tilesize"]

    def update(
        self,
        player_pos: vec,
        mob_count,
        mob_max: int,
        all_sprites,
        mobs: pg.sprite.Group,
    ) -> int:
        """
        Tracks distance to player and calls spawn function
        when appropriate.
        """
        self.target_dist = player_pos - self.pos
        if (
            self.settings["gen"]["spawn_min_dist"] ** 2
            < self.target_dist.length_squared()
            < self.settings["gen"]["spawn_max_dist"] ** 2
            and mob_count < mob_max
        ):
            return self.spawn(all_sprites, mobs)
        return 0

    def spawn(self, all_sprites, mobs: pg.sprite.Group) -> int:
        """
        Spawns enemies pseudo-randomly in an 8x8 tile area
        centered on the Spawner.
        Returns count of enemies spawned.
        """
        max_count = randint(
            self.settings["gen"]["spawn_min"],
            self.settings["gen"]["spawn_max"],
        )
        count = 0
        for row in range(self.rows - 4, self.rows + 4):
            for col in range(self.cols - 4, self.cols + 4):
                if col <= self.settings["lvl"]["tiles_wide"]:
                    if count >= max_count:
                        break
                    elif self.level_data[row][col] == "." and random() < 0.25:
                        if random() < 0.5:
                            mob = Mob(
                                self.settings,
                                self.img,
                                "sleeper",
                                col,
                                row,
                            )
                        else:
                            mob = Mob(
                                self.settings,
                                self.img,
                                "thrall",
                                col,
                                row,
                            )
                        all_sprites.add(mob)
                        mobs.add(mob)
                        count += 1
        self.kill()
        return count

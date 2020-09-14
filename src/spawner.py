# Copyright (c) 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
from random import randint, random
from src.sprites.sprites import Mob, Player

vec = pg.math.Vector2


class Spawner(pg.sprite.Sprite):
    """
    Spawner objects are placed on the map; when the player is within a certain distance,
    and if there are not already too many mobs present, the spawner will spawn mobs. 
    """

    def __init__(self, game, col, row):
        self.game = game
        self.groups = game.spawners
        pg.sprite.Sprite.__init__(self, self.groups)
        self.cols, self.rows = col, row
        self.pos = vec(col, row) * game.settings["gen"]["tilesize"]

    def update(self):
        """
        Tracks distance to player and calls spawn function
        when appropriate. 
        """
        self.target_dist = self.game.player.pos - self.pos
        if (
            self.game.settings["gen"]["spawn_min_dist"] ** 2
            < self.target_dist.length_squared()
            < self.game.settings["gen"]["spawn_max_dist"] ** 2
            and self.game.mob_count < self.game.mob_max
        ):
            self.spawn()

    def spawn(self):
        """
        Spawns enemies pseudo-randomly in an 8x8 tile area
        centered on the Spawner. 
        """
        max_count = randint(
            self.game.settings["gen"]["spawn_min"],
            self.game.settings["gen"]["spawn_max"],
        )
        count = 0
        for row in range(self.rows - 4, self.rows + 4):
            for col in range(self.cols - 4, self.cols + 4):
                if col <= self.game.settings["lvl"]["tiles_wide"]:
                    if count >= max_count:
                        break
                    elif self.game.map.level_data[row][col] == "." and random() < 0.25:
                        if random() < 0.5:
                            Mob(self.game, "sleeper", col, row)
                        else:
                            Mob(self.game, "thrall", col, row)
                        count += 1
        self.game.mob_count += count
        self.kill()

# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml
from src.sprites.grouping import Grouping
from random import choice

vec = pg.math.Vector2


class Wall(pg.sprite.Sprite):
    """
    Walls come in three flavors:
    stops_bullets=True: visible walls
    stops_bullets=False: invisible walls
    stops_bullets="Rift": Rift
    """

    def __init__(
        self,
        settings: ruamel.yaml.comments.CommentedMap,
        sprite_groups: Grouping,
        pos: vec,
        stops_bullets: bool,
    ):
        self.settings = settings
        self._layer = self.settings["layer"]["wall"]
        if stops_bullets == "Rift":
            self.groups = (
                sprite_groups.all_sprites,
                sprite_groups.walls,
                sprite_groups.stops_bullets,
            )
        elif stops_bullets == True:
            self.groups = sprite_groups.walls, sprite_groups.stops_bullets
        else:
            self.groups = sprite_groups.walls
        self.stops_bullets = stops_bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.rect = pg.Rect(
            0,
            0,
            self.settings["gen"]["tilesize"],
            self.settings["gen"]["tilesize"],
        )
        self.rect.topleft = self.pos


class Rift(Wall):
    """
    Rifts allow players to move between levels.
    Rifts track distance to player to determine whether
    the player is within distance to use.
    """

    def __init__(
        self,
        settings: ruamel.yaml.comments.CommentedMap,
        sprite_groups: Grouping,
        game_client_data_rift_img: pg.Surface,
        pos: vec,
    ):
        Wall.__init__(self, settings, sprite_groups, pos, "Rift")
        self.image = game_client_data_rift_img

    def check_usable(self, player_pos):
        self.target_dist = player_pos - self.pos
        if (
            self.target_dist.length_squared()
            < self.settings["lvl"]["rift_usable_distance"] ** 2
        ):
            return True
        return False

    def update(
        self, player_pos: vec, game_level: "Game.level()", game_client_data_biomes: list
    ):
        if self.check_usable(player_pos):
            keys = pg.key.get_pressed()
            if keys[pg.K_e]:
                # current method of switching levels does not retain player data
                game_level("gen", choice(game_client_data_biomes))
            if keys[pg.K_r]:
                game_level("temple.txt", "void")

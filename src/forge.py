# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml
from random import choice, random
from os import path
from src.sprites.sprites import *
from src.sprites.grouping import Grouping
from src.sprites.player import Player
from src.sprites.item import Item
from src.sprites.wall import Wall, Rift
from src.sprites.spawner import Spawner
from src.loader import Loader

vec = pg.math.Vector2


class Forge:
    """
    Forge class can be used to initalize and render map surfaces from text files.
    Forge is capable of splicing together multiple preset dungeon pieces.
    """

    def __init__(
        self,
        settings: ruamel.yaml.comments.CommentedMap,
        sprite_grouping: Grouping,
        client_data: Loader,
        character: str,
        player: Player,
        lvl_pieces=1,
    ):
        (
            self.client_data,
            self.sprite_grouping,
            self.character,
            self.player,
            self.settings,
        ) = (
            client_data,
            sprite_grouping,
            character,
            player,
            settings,
        )
        self.forge_data, self.level_data, self.rot, self.max_size = (
            {},
            [],
            [0, 90, 180, 270],
            lvl_pieces,
        )

    def new_surface(self, tiles_wide: int, tiles_high: int):
        """
        Creates a new surface, sized according to game settings.
        """
        self.width = tiles_wide * self.settings["gen"]["tilesize"]
        self.height = tiles_high * self.settings["gen"]["tilesize"] * self.max_size
        # https://stackoverflow.com/questions/328061/how-to-make-a-surface-with-a-transparent-background-in-pygame#328067
        self.temp_surface = pg.Surface(
            (self.width, self.height), pg.SRCALPHA, 32
        ).convert_alpha()

    def load_all(self):
        """
        Loads all textual data from map piece files.
        """
        for piece in self.settings["map"]["basic"]:
            self.load(piece)

    def load(self, piece: int):
        """
        Loads textual data from a given map piece file.
        """
        self.forge_data[piece] = []
        with open(path.join(self.client_data.map_folder, piece), "rt") as f:
            for line in f:
                self.forge_data[piece].append(line.strip("\n"))

    def build_lvl(self, biome: str):
        """
        Randomly grabs dungeon pieces and renders them onto the map surface next to one another.
        """
        for i in range(0, self.max_size):
            # https://stackoverflow.com/questions/4859292/how-to-get-a-random-value-in-python-dictionary
            piece = choice(list(self.forge_data.keys()))
            self.render(self.temp_surface, self.forge_data[piece], biome, i)
            self.level_data.extend(self.forge_data[piece])

    def render(self, surface: pg.Surface, piece: list, biome: str, i: int):
        """
        Renders the map from the textual data onto the pygame surface tile by tile
        and places sprites onto the map based on text flags.
        """
        y_offset = i * 32
        row_offset = y_offset * self.settings["gen"]["tilesize"]
        for row, tiles in enumerate(piece):
            y = row
            row *= self.settings["gen"]["tilesize"]
            for col, tile in enumerate(tiles):
                x = col
                col *= self.settings["gen"]["tilesize"]
                if tile != " " and tile != "0":
                    self.floor_img = pg.transform.rotate(
                        choice(self.client_data.floor_img[biome]), choice(self.rot)
                    )
                    surface.blit(self.floor_img, (col, row + row_offset))
                if tile == "1":
                    surface.blit(self.client_data.wall_img, (col, row + row_offset))
                if tile == "0":
                    Wall(
                        self.settings,
                        self.sprite_grouping,
                        vec(x, y + y_offset) * self.settings["gen"]["tilesize"],
                        False,
                    )
                if tile == "1":
                    Wall(
                        self.settings,
                        self.sprite_grouping,
                        vec(x, y + y_offset) * self.settings["gen"]["tilesize"],
                        True,
                    )
                if tile == "y" and i == 0:
                    Wall(
                        self.settings,
                        self.sprite_grouping,
                        vec(x, y + y_offset) * self.settings["gen"]["tilesize"],
                        False,
                    )
                if tile == "x" and i == self.max_size - 1:
                    Wall(
                        self.settings,
                        self.sprite_grouping,
                        vec(x, y + y_offset) * self.settings["gen"]["tilesize"],
                        True,
                    )
                    surface.blit(self.client_data.wall_img, (col, row + row_offset))
                if tile == "R" and i == 0:
                    Rift(
                        self.settings,
                        self.sprite_grouping,
                        self.client_data.rift_img,
                        vec(x, y + y_offset) * self.settings["gen"]["tilesize"],
                    )
                if tile == "M":
                    Spawner(
                        self.settings,
                        self.sprite_grouping,
                        self.level_data,
                        self.client_data.mob_img,
                        x,
                        y + y_offset,
                    )
                if tile == "p":
                    Item(
                        self.settings,
                        (self.sprite_grouping.all_sprites, self.sprite_grouping.items),
                        self.client_data.item_img,
                        vec(x, y + y_offset) * self.settings["gen"]["tilesize"],
                        "redpotion",
                        "hp",
                    )
                if tile == "P" and i == self.max_size - 1:
                    self.player.place(col, row + row_offset)

    def make_map(self) -> pg.Surface:
        """
        Used to access the map surface after map creation.
        """
        return self.temp_surface

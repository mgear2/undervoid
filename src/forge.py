# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
from random import choice, random
from os import path
from src.sprites import Mob, Wall, Player, pMove, Item, Rift
from src.spawner import Spawner

vec = pg.math.Vector2


class Forge:
    """
    Forge class can be used to initalize and render map surfaces from text files.
    Forge is capable of splicing together multiple preset dungeon pieces. 
    """

    def __init__(self, game, size):
        self.game = game
        self.data = {}
        self.level_data = []
        self.rot = [0, 90, 180, 270]
        self.max_size = size

    def new_surface(self, tiles_wide, tiles_high):
        """
        Creates a new surface, sized according to game settings. 
        """
        self.width = tiles_wide * self.game.settings["gen"]["tilesize"]
        self.height = tiles_high * self.game.settings["gen"]["tilesize"] * self.max_size
        # https://stackoverflow.com/questions/328061/how-to-make-a-surface-with-a-transparent-background-in-pygame#328067
        self.temp_surface = pg.Surface(
            (self.width, self.height), pg.SRCALPHA, 32
        ).convert_alpha()

    def load_all(self):
        """
        Loads all textual data from map piece files. 
        """
        for piece in self.game.settings["map"]["basic"]:
            self.load(piece)

    def load(self, piece):
        """
        Loads textual data from a given map piece file. 
        """
        self.data[piece] = []
        with open(path.join(self.game.client.data.map_folder, piece), "rt") as f:
            for line in f:
                self.data[piece].append(line.strip("\n"))

    def build_lvl(self, biome):
        """
        Randomly grabs dungeon pieces and renders them onto the map surface next to one another. 
        """
        for i in range(0, self.max_size):
            # https://stackoverflow.com/questions/4859292/how-to-get-a-random-value-in-python-dictionary
            piece = choice(list(self.data.keys()))
            self.render(self.temp_surface, self.data[piece], biome, i)
            self.level_data.extend(self.data[piece])

    def render(self, surface, piece, biome, i):
        """
        Renders the map from the textual data onto the pygame surface tile by tile
        and places sprites onto the map based on text flags. 
        """
        y_offset = i * 32
        row_offset = y_offset * self.game.settings["gen"]["tilesize"]
        for row, tiles in enumerate(piece):
            y = row
            row *= self.game.settings["gen"]["tilesize"]
            for col, tile in enumerate(tiles):
                x = col
                col *= self.game.settings["gen"]["tilesize"]
                if tile != " " and tile != "0":
                    self.floor_img = pg.transform.rotate(
                        choice(self.game.client.data.floor_img[biome]), choice(self.rot)
                    )
                    surface.blit(self.floor_img, (col, row + row_offset))
                if tile == "1":
                    surface.blit(
                        self.game.client.data.wall_img, (col, row + row_offset)
                    )
                if tile == "0":
                    Wall(
                        self.game,
                        vec(x, y + y_offset) * self.game.settings["gen"]["tilesize"],
                        False,
                    )
                if tile == "1":
                    Wall(
                        self.game,
                        vec(x, y + y_offset) * self.game.settings["gen"]["tilesize"],
                        True,
                    )
                if tile == "y" and i == 0:
                    Wall(
                        self.game,
                        vec(x, y + y_offset) * self.game.settings["gen"]["tilesize"],
                        False,
                    )
                if tile == "x" and i == self.max_size - 1:
                    Wall(
                        self.game,
                        vec(x, y + y_offset) * self.game.settings["gen"]["tilesize"],
                        True,
                    )
                    surface.blit(
                        self.game.client.data.wall_img, (col, row + row_offset)
                    )
                if tile == "R" and i == 0:
                    Rift(
                        self.game,
                        vec(x, y + y_offset) * self.game.settings["gen"]["tilesize"],
                    )
                if tile == "P" and i == self.max_size - 1:
                    if self.game.init_player:
                        self.game.player = self.game.client.player = Player(
                            self.game, col, row + row_offset
                        )
                        self.game.pmove = self.game.client.pmove = pMove(
                            self.game, col, row + row_offset
                        )
                        self.game.init_player = False
                    else:
                        self.game.player.place(col, row + row_offset)
                        self.game.pmove.place(col, row + row_offset)
                if tile == "M":
                    Spawner(self.game, x, y + y_offset)
                if tile == "p":
                    Item(
                        self.game,
                        vec(x, y + y_offset) * self.game.settings["gen"]["tilesize"],
                        "redpotion",
                        "hp",
                    )

    def make_map(self):
        """
        Used to access the map surface after map creation. 
        """
        return self.temp_surface

# Copyright (c) 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Building off example code from
# https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap

import pygame as pg
from random import choice, randint, random
from os import sys, path
from sprites import Mob, Wall, Player, pMove, Item

vec = pg.math.Vector2


class Map:
    def __init__(self, game, filename):
        self.data = []
        self.game = game
        with open(filename, "rt") as f:
            for line in f:
                self.data.append(line.strip("\n"))
        tiles_wide = max(len(elem) for elem in self.data)
        self.tile_width = tiles_wide
        self.tile_height = len(self.data)
        self.width = self.tile_width * self.game.settings["gen"]["tilesize"]
        self.height = self.tile_height * self.game.settings["gen"]["tilesize"]
        self.rot = [0, 90, 180, 270]

    def render(self, surface):
        for row, tiles in enumerate(self.data):
            row *= self.game.settings["gen"]["tilesize"]
            for col, tile in enumerate(tiles):
                col *= self.game.settings["gen"]["tilesize"]
                if tile != " " and tile != "0":
                    self.floor_img = pg.transform.rotate(
                        choice(self.game.floor_img), choice(self.rot)
                    )
                    surface.blit(self.floor_img, (col, row))
                if tile == "1":
                    surface.blit(self.game.wall_img, (col, row))

    def make_map(self):
        # https://stackoverflow.com/questions/328061/how-to-make-a-surface-with-a-transparent-background-in-pygame#328067
        temp_surface = pg.Surface(
            (self.width, self.height), pg.SRCALPHA, 32
        ).convert_alpha()
        self.render(temp_surface)
        return temp_surface


class Forge:
    def __init__(self, game):
        self.game = game
        self.data = {}
        self.return_data = []
        self.rot = [0, 90, 180, 270]
        self.max_size = 3  # self.max_size = self.game.settings["gen"]["lvl_size"]
        self.load_all()

    def new_lvl(self):
        # https://stackoverflow.com/questions/30902558/finding-the-longest-list-in-a-list-of-lists-in-python
        self.tiles_w = self.game.settings["lvl"]["tiles_wide"]
        self.tiles_h = self.game.settings["lvl"]["tiles_high"]
        self.width = self.tiles_w * self.game.settings["gen"]["tilesize"]
        self.height = (
            self.tiles_h * self.game.settings["gen"]["tilesize"] * self.max_size
        )
        # https://stackoverflow.com/questions/328061/how-to-make-a-surface-with-a-transparent-background-in-pygame#328067
        self.temp_surface = pg.Surface(
            (self.width, self.height), pg.SRCALPHA, 32
        ).convert_alpha()

    def load_all(self):
        for piece in self.game.settings["map"]["basic"]:
            self.load(piece)

    def load(self, piece):
        self.data[piece] = []
        with open(path.join(self.game.map_folder, piece), "rt") as f:
            for line in f:
                self.data[piece].append(line.strip("\n"))

    def build_lvl(self):
        for i in range(0, self.max_size):
            piece = "map_gen01.txt"
            print(self.data[piece])
            self.render(self.temp_surface, self.data[piece], i)
        self.return_data.append(self.data[piece])

    def render(self, surface, piece, i):
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
                        choice(self.game.floor_img), choice(self.rot)
                    )
                    surface.blit(self.floor_img, (col, row + row_offset))
                if tile == "1":
                    print("blitting {}, {}".format(col, row + row_offset))
                    surface.blit(self.game.wall_img, (col, row + row_offset))
                    Wall(
                        self.game,
                        vec(x, y + y_offset) * self.game.settings["gen"]["tilesize"],
                        True,
                    )
                if tile == "0":
                    Wall(
                        self.game,
                        vec(x, y + y_offset) * self.game.settings["gen"]["tilesize"],
                        False,
                    )
                if tile == "R" and i == 0:
                    print("RIFT: unimplemented")
                if tile == "P" and i == self.max_size - 1:
                    print("PLAYER {}, {}".format(x, y + y_offset))
                    self.game.player = Player(self.game, x, y + y_offset)
                    self.game.pmove = pMove(self.game, x, y + y_offset)
                if tile == "M":
                    Mob(self.game, "thrall", x, y + y_offset)
                    # Spawner(self, col, row + y_offset)
                if tile == "p":
                    Item(
                        self.game,
                        vec(x, y + y_offset) * self.game.settings["gen"]["tilesize"],
                        "redpotion",
                        "hp",
                    )

    def make_map(self):
        print(self.temp_surface)
        return self.temp_surface


class Camera:
    def __init__(self, game, width, height, cursor):
        self.game = game
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.cursor = cursor

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.game.settings["gen"]["width"] / 2)
        y = -target.rect.centery + int(self.game.settings["gen"]["height"] / 2)
        self.camera = pg.Rect(x, y, self.width, self.height)
        self.cursor.rect.centerx -= x
        self.cursor.rect.centery -= y
        self.cursor.pos = self.cursor.rect.center


class Spawner(pg.sprite.Sprite):
    def __init__(self, game, col, row):
        self.game = game
        self.groups = game.spawners
        pg.sprite.Sprite.__init__(self, self.groups)
        self.cols, self.rows = col, row
        self.pos = vec(col, row) * game.settings["gen"]["tilesize"]

    def update(self):
        self.target_dist = self.game.player.pos - self.pos
        if (
            self.game.settings["gen"]["spawn_min_dist"] ** 2
            < self.target_dist.length_squared()
            < self.game.settings["gen"]["spawn_max_dist"] ** 2
            and self.game.mob_count < self.game.mob_max
        ):
            self.spawn()

    def spawn(self):
        max_count = randint(
            self.game.settings["gen"]["spawn_min"],
            self.game.settings["gen"]["spawn_max"],
        )
        count = 0
        for row in range(self.rows - 4, self.rows + 4):
            for col in range(self.cols - 4, self.cols + 4):
                if count >= max_count:
                    break
                elif self.game.map.data[row][col] == "." and random() < 0.25:
                    if random() < 0.5:
                        Mob(self.game, "sleeper", col, row)
                    else:
                        Mob(self.game, "thrall", col, row)
                    count += 1
        self.game.mob_count += count
        self.kill()

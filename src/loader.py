# Copyright (c) 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
from os import path


class Loader:
    def __init__(self, settings):
        self.settings = settings

    def build_path(self):
        """
        Builds a directory structure for the game. 
        """
        self.game_folder = path.dirname(__file__)
        self.data_folder = path.join(self.game_folder, "../data")
        self.img_folder = path.join(self.data_folder, "img")
        self.map_folder = path.join(self.data_folder, "maps")
        self.music_folder = path.join(self.data_folder, "music")
        self.sound_folder = path.join(self.data_folder, "sounds")
        self.fonts_folder = path.join(self.data_folder, "fonts")

    def load_img(self, source, scale, alpha):
        """
        Used to load images from source files, scale them, and convert() or convert_alpha() as specified. 
        """
        img = pg.image.load(path.join(self.img_folder, source))
        img = pg.transform.scale(img, scale)
        if alpha:
            img = img.convert_alpha()
        else:
            img = img.convert()
        return img

    def load_data(self):
        """
        Initializes and populates lists and dictionaries of game data. 
        Initializes mouse settings and game icon. 
        Still stands to be refactored and optimized further. 
        """
        self.cursor_img = []
        self.weapon_vfx = []
        self.floor_img = {}
        self.player_img = {}
        self.mob_img = {}
        self.mob_img["base"], self.mob_img["grave"] = {}, {}
        self.item_img = {}
        self.sounds = {}
        self.stances = ["magic", "coachgun"]
        self.characters = ["pilgrim", "voidwalker", "lizardwizard"]
        self.mob_kinds = ["thrall", "sleeper"]
        self.biomes = ["dungeon", "dungeon", "void"]
        tilesize = (self.settings["gen"]["tilesize"], self.settings["gen"]["tilesize"])

        # System Images
        self.undervoid_icon = self.load_img(
            self.settings["img"]["icon"], (64, 64), True
        )
        self.title_art = self.load_img(
            self.settings["img"]["title"],
            tuple(self.settings["gen"]["titledim"]),
            False,
        )
        self.rift_img = self.load_img(self.settings["img"]["rift"], tilesize, False)
        for img in self.settings["img"]["cursor"]:
            self.cursor_img.append(self.load_img(img, (64, 64), True))

        # Environment Images
        self.wall_img = self.load_img(
            self.settings["img"]["wall"]["voidwall"], tilesize, False
        )
        for biome in self.biomes:
            self.floor_img[biome] = []
            for img in self.settings["img"]["floor"][biome]:
                self.floor_img[biome].append(self.load_img(img, tilesize, False))

        # Player Images
        for character in self.characters:
            self.player_img[character] = {}
            for stance in self.stances:
                self.player_img[character][stance] = self.load_img(
                    self.settings["img"]["player"][character]["stance"][stance],
                    tuple((2 * x) for x in tilesize),
                    True,
                )
            self.player_img[character]["move"] = []
            for img in self.settings["img"]["player"][character]["move"]:
                self.player_img[character]["move"].append(
                    self.load_img(img, tuple((2 * x) for x in tilesize), True)
                )

        # Bullet Images
        self.vbullet_img = self.load_img(
            self.settings["img"]["bullets"]["void"]["bullet"], tilesize, True
        )
        for img in self.settings["img"]["bullets"]["void"]["fx"]:
            self.weapon_vfx.append(self.load_img(img, tilesize, True))

        # Mob Images
        for kind in self.mob_kinds:
            self.mob_img["base"][kind] = self.load_img(
                self.settings["img"]["mob"][kind]["main"], tilesize, True
            )
            self.mob_img["grave"][kind] = []
            for img in self.settings["img"]["mob"][kind]["grave"]:
                self.mob_img["grave"][kind].append(self.load_img(img, tilesize, True))

        # Item Images
        for item in self.settings["img"]["items"]:
            self.item_img[item] = self.load_img(
                self.settings["img"]["items"][item],
                # https://stackoverflow.com/questions/1781970/multiplying-a-tuple-by-a-scalar
                tuple(int(0.75 * x) for x in tilesize),
                True,
            )

        # Sounds
        for sound in self.settings["sounds"]:
            self.sounds[sound] = pg.mixer.Sound(
                path.join(self.sound_folder, self.settings["sounds"][sound])
            )

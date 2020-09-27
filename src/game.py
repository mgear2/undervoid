# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import sys
import ruamel.yaml
from os import path, environ
from src.sprites.sprites import *
from src.sprites.cursor import Cursor
from src.forge import Forge
from src.spawner import Spawner
from src.camera import Camera
from random import random, randint

yaml = ruamel.yaml.YAML()


class Game:
    """
    Overarching Game class; loads and manipulates game data and runs the main game loop.
    """

    def __init__(self, client):
        """
        Initializes sprite groups, builds initial level,
        specifies variables to be used for morphing background color.
        """
        self.client = client
        self.player, self.pmove, self.character, self.map = (
            self.client.player,
            None,
            self.client.character,
            None,
        )
        with open("settings.yaml") as f:
            self.settings = yaml.load(f)
            f.close()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.pmove_sprite = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.stops_bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.graves = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        self.cursor_sprite = pg.sprite.Group()
        self.weaponvfx_sprite = pg.sprite.Group()
        self.spawners = pg.sprite.Group()
        self.init_player = True
        self.level("temple.txt", "void")
        # https://stackoverflow.com/questions/51973441/how-to-fade-from-one-colour-to-another-in-pygame
        self.base_color = choice(self.settings["void_colors"])
        self.next_color = choice(self.settings["void_colors"])
        self.change_every_x_seconds = 2
        self.number_of_steps = self.change_every_x_seconds * self.settings["gen"]["fps"]
        self.step = 1

    def level(self, target_lvl, biome):
        """
        Utilizes the Forge class to build and returns a level with the desired specifications.
        If the level is "gen", a new level will be generated. Otherwise, Forge will attempt to
        load a map from the specified file.
        """
        for sprite in self.all_sprites:
            if sprite != self.client.player and sprite != self.client.pmove:
                sprite.kill()
        for wall in self.walls:
            wall.kill()
        for spawner in self.spawners:
            spawner.kill()
        if target_lvl == "gen":
            lvl_pieces, surf_w, surf_h = (
                self.settings["lvl"]["pieces"],
                self.settings["lvl"]["tiles_wide"],
                self.settings["lvl"]["tiles_high"],
            )
        else:
            lvl_pieces, surf_w, surf_h = 1, 128, 128
        self.map = Forge(
            self.client.data,
            self.all_sprites,
            self.walls,
            self.stops_bullets,
            self.character,
            self.player_sprite,
            self.pmove_sprite,
            self.init_player,
            self.player,
            self.pmove,
            self.items,
            self.spawners,
            self.mobs,
            self.settings,
            lvl_pieces,
        )
        if target_lvl == "gen":
            self.map.load_all()
        else:
            self.map.load(target_lvl)
            if target_lvl == "temple.txt" and not self.init_player:
                self.client.player.hp = self.client.player.max_hp
        self.map.new_surface(surf_w, surf_h)
        if self.init_player:
            self.init_player = False
        self.map.build_lvl(biome)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.cursor = Cursor(
            self.settings,
            self.all_sprites,
            self.cursor_sprite,
            self.client.data.cursor_img,
        )
        self.camera = Camera(
            self.settings, self.map.width, self.map.height, self.cursor
        )
        self.player = self.client.player = self.map.player
        self.pmove = self.client.pmove = self.map.pmove
        self.mob_count = 0
        self.mob_max = self.settings["gen"]["mob_max"]

    def update(self):
        """
        Updates sprites, spawners and camera.
        Checks for player hitting items and resolves hits.
        Checks for mobs hitting player and resolves hits.
        Checks for bullets hitting mobs and resolves hits.
        Morphs the background color one step.
        """
        # self.all_sprites.update()

        self.walls.update(self.client.player.pos, self.level, self.client.data.biomes)
        self.stops_bullets.update(
            self.client.player.pos, self.level, self.client.data.biomes
        )
        for mob in self.mobs:
            self.mob_count += mob.update(
                self.client.player.pos,
                self.client.data.mob_img,
                self.client.data.sounds,
                self.client.dt,
                self.walls,
                self.graves,
                self.items,
                self.client.data.item_img,
                self.mob_count,
            )
        self.bullets.update(self.client.dt)
        self.graves.update()
        self.items.update()
        self.player_sprite.update(
            self.cursor.pos,
            self.client.data.sounds["wave01"],
            self.client.data.player_img[self.client.character]["magic"],
            self.client.dt,
            self.walls,
            self.bullets,
            self.client.data.vbullet_img,
            self.stops_bullets,
            self.weaponvfx_sprite,
            self.client.data.weapon_vfx,
        )
        self.cursor_sprite.update()
        self.weaponvfx_sprite.update()
        self.pmove_sprite.update(self.client.player.vel, self.client.player.pos)
        for spawner in self.spawners:
            self.mob_count += spawner.update(
                self.player.pos, self.mob_count, self.mob_max
            )
        self.camera.update(self.client.player)
        # player hits items
        hits = pg.sprite.spritecollide(
            self.client.player, self.items, False, collide_hit_rect
        )
        for hit in hits:
            if (
                hit.kind == "hp"
                and self.client.player.hp < self.settings["player"]["hp"]
            ):
                hit.kill()
                if self.settings["gen"]["sound"] == "on":
                    self.client.sounds["treasure02"].play()
                self.client.player.add_hp(
                    self.settings["items"]["potions"]["red"]["hp"]
                    * self.client.player.max_hp
                )
            if hit.kind == "gp":
                hit.kill()
                if self.settings["gen"]["sound"] == "on":
                    self.client.sounds["treasure03"].play()
                self.client.player.coins += 1
        # mobs hitting player
        hits = pg.sprite.spritecollide(
            self.client.player, self.mobs, False, collide_hit_rect
        )
        for hit in hits:
            now = pg.time.get_ticks()
            if now - hit.last_hit > self.settings["mob"]["thrall"]["dmg_rate"]:
                hit.last_hit = now
                self.client.player.hp -= self.settings["mob"]["thrall"]["dmg"]
                hit.vel = vec(0, 0)
                self.client.player.pos += vec(
                    self.settings["mob"]["thrall"]["knockback"], 0
                ).rotate(-hits[0].rot)
                if self.settings["gen"]["sound"] == "on":
                    self.client.sounds[(choice(self.settings["hit_sounds"]))].play()
            elif random() < 0.5:  # enemies get bounced back on ~50% of failed hits
                hit.pos += vec(self.settings["mob"]["thrall"]["knockback"], 0).rotate(
                    hits[0].rot
                )
        # bullets hitting mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.hp -= (
                self.settings["weapon"]["vbullet"]["dmg"]
                * self.settings["player"]["dmg_mult"]
            )
            # hit.vel = vec(0, 0)
        # https://stackoverflow.com/questions/51973441/how-to-fade-from-one-colour-to-another-in-pygame
        self.step += 1
        if self.step < self.number_of_steps:
            self.current_color = [
                x + (((y - x) / self.number_of_steps) * self.step)
                for x, y in zip(
                    pg.color.Color(self.base_color), pg.color.Color(self.next_color)
                )
            ]
        else:
            self.step = 1
            self.base_color = self.next_color
            self.next_color = choice(self.settings["void_colors"])
        self.bg_color = self.current_color

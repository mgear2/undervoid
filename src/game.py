# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import sys
import ruamel.yaml
from os import path, environ
from src.sprites.player import Player
from src.sprites.sprites import *
from src.sprites.item import Item
from src.sprites.grave import Grave
from src.sprites.cursor import Cursor
from src.sprites.grouping import Grouping
from src.forge import Forge
from src.sprites.spawner import Spawner
from src.camera import Camera
from src.loader import Loader
from random import random, randint

yaml = ruamel.yaml.YAML()


class Game:
    """
    Overarching Game class; loads and manipulates game data and runs the main game loop.
    """

    def __init__(self, data: Loader, character: str):
        """
        Initializes sprite groups, builds initial level,
        specifies variables to be used for morphing background color.
        """
        self.data, self.character, self.player, self.map = data, character, None, None
        with open("settings.yaml") as f:
            self.settings = yaml.load(f)
            f.close()
        self.sprite_grouping = Grouping()
        self.init_player = True
        self.level("temple.txt", "void")
        # https://stackoverflow.com/questions/51973441/how-to-fade-from-one-colour-to-another-in-pygame
        self.base_color = choice(self.settings["void_colors"])
        self.next_color = choice(self.settings["void_colors"])
        self.change_every_x_seconds = 2
        self.number_of_steps = self.change_every_x_seconds * self.settings["gen"]["fps"]
        self.step = 1

    def level(self, target_lvl, biome: str):
        """
        Utilizes the Forge class to build and returns a level with the desired specifications.
        If the level is "gen", a new level will be generated. Otherwise, Forge will attempt to
        load a map from the specified file.
        """
        for sprite in self.sprite_grouping.all_sprites:
            if sprite != self.player and sprite != self.player.legs:
                sprite.kill()
        for wall in self.sprite_grouping.walls:
            wall.kill()
        for spawner in self.sprite_grouping.spawners:
            spawner.kill()
        if target_lvl == "gen":
            lvl_pieces, surf_w, surf_h = (
                self.settings["lvl"]["pieces"],
                self.settings["lvl"]["tiles_wide"],
                self.settings["lvl"]["tiles_high"],
            )
        else:
            lvl_pieces, surf_w, surf_h = 1, 128, 128
        if self.init_player:
            self.init_player = False
            self.player = Player(
                self.settings,
                self.data.player_img[self.character]["magic"],
                self.data.player_img[self.character]["move"],
            )
            self.sprite_grouping.all_sprites.add(self.player, self.player.legs)
            self.sprite_grouping.player_sprite.add(self.player)
            self.sprite_grouping.legs_sprite.add(self.player.legs)
        self.map = Forge(
            self.settings,
            self.sprite_grouping,
            self.data,
            self.character,
            self.player,
            lvl_pieces,
        )
        if target_lvl == "gen":
            self.map.load_all()
        else:
            self.map.load(target_lvl)
            if target_lvl == "temple.txt" and not self.init_player:
                self.player.hp = self.player.max_hp
        self.map.new_surface(surf_w, surf_h)
        self.map.build_lvl(biome)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.cursor = Cursor(
            self.settings,
            self.data.cursor_img,
        )
        self.sprite_grouping.all_sprites.add(self.cursor)
        self.sprite_grouping.cursor_sprite.add(self.cursor)
        self.camera = Camera(
            self.settings, self.map.width, self.map.height, self.cursor
        )
        self.player = self.map.player
        self.mob_count, self.mob_max = 0, self.settings["gen"]["mob_max"]

    def update(self, dt: float):
        """
        Updates sprites, spawners and camera.
        Checks for player hitting items and resolves hits.
        Checks for mobs hitting player and resolves hits.
        Checks for bullets hitting mobs and resolves hits.
        Morphs the background color one step.
        """
        self.sprite_grouping.rifts.update(self.player.pos, self.level, self.data.biomes)
        self.handle_mobs(dt)
        self.sprite_grouping.bullets.update(
            dt, self.sprite_grouping.bullets, self.sprite_grouping.stops_bullets
        )
        self.sprite_grouping.items.update()
        self.handle_player(dt)
        self.sprite_grouping.cursor_sprite.update()
        self.sprite_grouping.weaponvfx_sprite.update()
        self.sprite_grouping.legs_sprite.update(self.player.vel, self.player.pos)
        for spawner in self.sprite_grouping.spawners:
            self.mob_count += spawner.update(
                self.player.pos,
                self.mob_count,
                self.mob_max,
                self.sprite_grouping.all_sprites,
                self.sprite_grouping.mobs,
            )
        self.camera.update(self.player)
        self.handle_item_hits()
        self.handle_mob_hits()
        self.handle_bullet_hits()
        self.handle_background_fade()

    def handle_player(self, dt: float):
        """
        Helper function which handles player updates with bullet and vfx sprite group additions.
        """
        for player_sprite in self.sprite_grouping.player_sprite:
            bullet, vfx = player_sprite.update(
                self.cursor.pos,
                self.data.sounds["wave01"],
                self.data.player_img[self.character]["magic"],
                dt,
                self.data.vbullet_img,
                self.data.weapon_vfx,
                self.sprite_grouping.walls,
            )
            if bullet:
                self.sprite_grouping.all_sprites.add(bullet, vfx)
                self.sprite_grouping.bullets.add(bullet)
                self.sprite_grouping.weaponvfx_sprite.add(vfx)

    def handle_mobs(self, dt: float):
        """
        Helper function which handles mob updates, grave placement, and item drops.
        """
        for mob in self.sprite_grouping.mobs:
            alive, dropped_item = mob.update(
                self.player.pos,
                self.data.mob_img,
                self.data.sounds,
                dt,
                self.mob_count,
                self.sprite_grouping.mobs,
                self.sprite_grouping.walls,
            )
            if not alive:
                self.mob_count -= 1
                grave = Grave(
                    self.settings,
                    self.data.mob_img,
                    mob.kind,
                    mob.pos,
                    mob.rot,
                )
                self.sprite_grouping.all_sprites.add(grave)
                self.sprite_grouping.graves.add(grave)
                if dropped_item:
                    item = Item(
                        self.settings,
                        self.data.item_img,
                        mob.pos,
                        dropped_item[0],
                        dropped_item[1],
                    )
                    self.sprite_grouping.all_sprites.add(item)
                    self.sprite_grouping.items.add(item)
                mob.kill()

    def handle_item_hits(self):
        """
        Helper function which handles instances of the player hitting items.
        """
        hits = pg.sprite.spritecollide(
            self.player, self.sprite_grouping.items, False, collide_hit_rect
        )
        for hit in hits:
            if hit.kind == "hp" and self.player.hp < self.settings["player"]["hp"]:
                hit.kill()
                if self.settings["gen"]["sound"] == "on":
                    self.data.sounds["treasure02"].play()
                self.player.add_hp(
                    self.settings["items"]["potions"]["red"]["hp"] * self.player.max_hp
                )
            if hit.kind == "gp":
                hit.kill()
                if self.settings["gen"]["sound"] == "on":
                    self.data.sounds["treasure03"].play()
                self.player.coins += 1

    def handle_mob_hits(self):
        """
        Helper function which handles instances of mobs hitting the player.
        """
        hits = pg.sprite.spritecollide(
            self.player, self.sprite_grouping.mobs, False, collide_hit_rect
        )
        for hit in hits:
            now = pg.time.get_ticks()
            if now - hit.last_hit > self.settings["mob"]["thrall"]["dmg_rate"]:
                hit.last_hit = now
                self.player.hp -= self.settings["mob"]["thrall"]["dmg"]
                hit.vel = vec(0, 0)
                self.player.pos += vec(
                    self.settings["mob"]["thrall"]["knockback"], 0
                ).rotate(-hits[0].rot)
                if self.settings["gen"]["sound"] == "on":
                    self.data.sounds[(choice(self.settings["hit_sounds"]))].play()
            elif random() < 0.5:  # enemies get bounced back on ~50% of failed hits
                hit.pos += vec(self.settings["mob"]["thrall"]["knockback"], 0).rotate(
                    hits[0].rot
                )

    def handle_bullet_hits(self):
        """
        Helper function which handles instances of bullets hitting mobs.
        """
        hits = pg.sprite.groupcollide(
            self.sprite_grouping.mobs, self.sprite_grouping.bullets, False, True
        )
        for hit in hits:
            hit.hp -= (
                self.settings["weapon"]["vbullet"]["dmg"]
                * self.settings["player"]["dmg_mult"]
            )
            # hit.vel = vec(0, 0)

    def handle_background_fade(self):
        """
        Helper function which handles a single step of the continuous background color fade.
        Also see: https://stackoverflow.com/questions/51973441/how-to-fade-from-one-colour-to-another-in-pygame
        """
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

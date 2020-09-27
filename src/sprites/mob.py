# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml
from random import choice, random
from src.sprites.grave import Grave
from src.sprites.item import Item
from src.sprites.grouping import Grouping

vec = pg.math.Vector2


class Mob(pg.sprite.Sprite):
    """
    Mob class provides mob sprites and tracks mob instance data.
    """

    def __init__(
        self,
        settings: ruamel.yaml.comments.CommentedMap,
        sprite_grouping: Grouping,
        game_client_data_mob_img: pg.Surface,
        kind: str,
        x,
        y: int,
    ):
        self.settings = settings
        self.kind = kind
        self._layer = self.settings["layer"]["mob"]
        self.sprite_grouping = sprite_grouping
        self.groups = sprite_grouping.all_sprites, sprite_grouping.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game_client_data_mob_img["base"][kind].copy()
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.hit_rect = pg.Rect(
            0,
            0,
            self.settings["gen"]["tilesize"] / 2,
            self.settings["gen"]["tilesize"] / 2,
        )
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * self.settings["gen"]["tilesize"]
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.hp = self.settings["mob"][kind]["hp"]
        self.max_hp = self.settings["mob"][kind]["hp"]
        self.speed = self.settings["gen"]["tilesize"] * choice(
            self.settings["mob"][kind]["speed"]
        )
        self.triggered = False
        self.last_hit = 0
        self.items = [("redpotion", "hp"), ("coin", "gp")]

    def avoid_mobs(self):
        for mob in self.groups[1]:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < self.settings["gen"]["tilesize"] * 2:
                    self.acc += dist.normalize()

    def update(
        self,
        player_pos: vec,
        game_client_data_mob_img: dict,
        game_sounds: dict,
        game_client_dt: float,
        game_client_data_item_img: dict,
        mob_count: int,
    ) -> int:
        self.target_dist = player_pos - self.pos
        self.rot = self.target_dist.angle_to(vec(1, 0))
        self.image = pg.transform.rotate(
            game_client_data_mob_img["base"][self.kind], self.rot
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        if (
            self.triggered == False
            and self.target_dist.length_squared()
            < self.settings["mob"][self.kind]["player_radius"] ** 2
        ):
            self.triggered = True
            if self.settings["gen"]["sound"] == "on":
                game_sounds["growl01"].play()
        if self.triggered:
            # self.acc = vec(MOB['THRALL_SPEED'][0],0).rotate(-self.rot)
            if self.settings["gen"]["sound"] == "on" and random() < 0.0015:
                game_sounds["growl01"].play()
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            try:
                self.acc.scale_to_length(self.speed)
            except Exception as e:
                print("{}".format(e))
            self.acc += self.vel * -1
            self.vel += self.acc * game_client_dt
            # Equations of motion
            self.pos += (
                self.vel * game_client_dt + 0.5 * self.acc * game_client_dt ** 1.025
            )
            self.hit_rect.centerx = self.pos.x
            self.collide_with_walls(self, self.sprite_grouping.walls, "x")
            self.hit_rect.centery = self.pos.y
            self.collide_with_walls(self, self.sprite_grouping.walls, "y")
            self.rect.center = self.hit_rect.center
        if self.hp <= 0:
            Grave(
                self.settings,
                self.groups[0],
                self.sprite_grouping.graves,
                game_client_data_mob_img,
                self.kind,
                self.pos,
                self.rot,
            )
            if random() < self.settings["mob"][self.kind]["drop_chance"]:
                item = choice(self.items)
                Item(
                    self.settings,
                    self.groups[0],
                    self.sprite_grouping.items,
                    game_client_data_item_img,
                    self.pos,
                    item[0],
                    item[1],
                )
            self.kill()
            return -1
        return 0

    def collide_with_walls(
        self, sprite: pg.sprite.Sprite, group: pg.sprite.Group, dir: str
    ):
        """
        Used for collision detection between player/mobs and walls. Mobs are
        currently set to not be restricted by Void (invisible) walls, while the player is.
        """
        hits = pg.sprite.spritecollide(sprite, group, False, self.collide_hit_rect)
        if hits:
            if type(sprite) == Mob and not hits[0].stops_bullets:
                return
            if dir == "x":
                if hits[0].rect.centerx > sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
                if hits[0].rect.centerx < sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
            if dir == "y":
                if hits[0].rect.centery > sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
                if hits[0].rect.centery < sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y

    def collide_hit_rect(self, one: pg.sprite.Sprite, two: pg.sprite.Sprite):
        """
        Used for hit_rect collision:
        """
        return one.hit_rect.colliderect(two.rect)

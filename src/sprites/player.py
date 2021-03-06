# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml
from random import uniform, choice, random
from src.sprites.sprites import *
from src.sprites.bullet import Bullet
from src.sprites.legs import Legs
from src.sprites.weapon_vfx import Weapon_VFX
from src.sprites.legs import Legs

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    """
    Player class provides the player sprite and tracks all player data.
    """

    def __init__(
        self,
        settings: ruamel.yaml.comments.CommentedMap,
        player_img,
        legs_img: pg.Surface,
        x=0,
        y=0,
    ):
        self.settings, self._layer = (
            settings,
            settings["layer"]["player"],
        )
        pg.sprite.Sprite.__init__(self)
        self.stance = "magic"
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.hit_rect = pg.Rect(self.settings["player"]["hit_rect"])
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.max_hp = self.settings["player"]["hp"]
        self.hp = self.settings["player"]["hp"]
        self.speed = (
            self.settings["gen"]["tilesize"] * self.settings["player"]["speed_mult"]
        )
        self.coins = 0
        self.sound_on = self.settings["gen"]["sound"]
        self.legs = Legs(self.settings, legs_img)

    def place(self, x, y: int):
        self.pos = vec(x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.legs.place(x, y)

    def get_keys(
        self,
        game_cursor_pos: tuple,
    ) -> (vec, vec):
        """
        get_keys handles player velocity adjustment for movement keys and for attack keys generates
        a position and direction (vec, vec) to be returned for bullet placement
        """
        self.rot_speed, self.vel = 0, vec(0, 0)
        keys, mouse = pg.key.get_pressed(), pg.mouse.get_pressed()
        pos, direction = None, None
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = self.speed
        if keys[pg.K_SPACE] or mouse[0]:
            now = pg.time.get_ticks()
            if now - self.last_shot > self.settings["weapon"]["vbullet"]["rate"]:
                self.last_shot = now
                angle = (game_cursor_pos - self.pos).angle_to(vec(1, 0))
                direction = vec(1, 0).rotate(-angle)
                pos = self.pos + vec(self.settings["player"]["hand_offset"]).rotate(
                    -self.rot
                )
        if self.vel.x != 0 and self.vel.y != 0:
            # correct diagonal movement to be same speed
            # multiply by 1/sqrt(2)
            self.vel *= 0.70701
        return pos, direction

    def update(
        self,
        game_cursor_pos: tuple,
        game_sound: pg.mixer.Sound,
        game_client_data_player_img: pg.Surface,
        game_client_dt: float,
        game_client_data_bullet_img: pg.Surface,
        game_client_data_weaponvfx: list,
        walls: pg.sprite.Group,
    ) -> (pg.sprite.Sprite, pg.sprite.Sprite):
        pos, direction = self.get_keys(game_cursor_pos)
        bullet, vfx = None, None
        if pos:
            bullet = Bullet(
                self.settings,
                game_client_data_bullet_img,
                pos,
                direction,
                self.rot,
            )
            vfx = Weapon_VFX(
                self.settings,
                game_client_data_weaponvfx,
                self.pos
                + vec(self.settings["player"]["hand_offset"]).rotate(-self.rot),
            )
            if self.sound_on:  # and random() < 0.75:
                game_sound.play()
        self.rot = (game_cursor_pos - self.pos).angle_to(vec(1, 0)) % 360
        self.image = pg.transform.rotate(
            game_client_data_player_img,
            self.rot,
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * game_client_dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, walls, "y")
        self.rect.center = self.hit_rect.center
        return bullet, vfx

    def add_hp(self, amount: int):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

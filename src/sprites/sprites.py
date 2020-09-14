# Copyright (c) 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
from os import path
from random import uniform, choice, random
import pytweening as tween

from src.sprites.mob import Mob

vec = pg.math.Vector2


def collide_hit_rect(one, two):
    """
    Used for hit_rect collision:

    Drawn largely from:
    https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2023
    """
    return one.hit_rect.colliderect(two.rect)


def draw_hp(client, surface, x, y, pct, b_len, b_height, player):
    """
    Used to draw mob and player health bars.

    Inspired by:
    https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2023
    """
    if pct < 0:
        pct = 0
    if pct > 0.6:
        color = client.settings["colors"]["green"]
    elif pct > 0.3:
        color = client.settings["colors"]["yellow"]
    else:
        color = client.settings["colors"]["red"]
    fill = pct * b_len
    hp_bar = pg.Rect(x, y, fill, b_height)
    pg.draw.rect(surface, color, hp_bar)
    if player:
        outline_rect = pg.Rect(x, y, b_len, b_height)
        pg.draw.rect(surface, client.settings["colors"]["white"], outline_rect, 2)


def draw_score(client):
    """
    Draws the players score and a coin image in the lower right corner of the screen.
    """
    score = client.text_format(
        str(client.player.coins), client.font, 60, client.settings["colors"]["white"]
    )
    client.screen.blit(
        pg.transform.scale(client.data.item_img["coin"], (92, 92)),
        (client.settings["gen"]["width"] - 100, client.settings["gen"]["height"] - 100),
    )
    score_x = 75 + len(str(client.player.coins)) * 25
    client.screen.blit(
        score,
        (
            client.settings["gen"]["width"] - score_x,
            client.settings["gen"]["height"] - 70,
        ),
    )


def draw_fps(client):
    """
    Draws the fps in the upper left corner of the screen.
    """
    fontsize, line_y = 20, 15
    fps_text = client.text_format(
        "{:.2f}".format(client.clock.get_fps()),
        client.font,
        fontsize,
        client.settings["colors"]["white"],
    )
    client.screen.blit(
        fps_text,
        (
            line_y,
            line_y,
        ),
    )


def collide_with_walls(sprite, group, dir):
    """
    Used for collision detection between player/mobs and walls. Mobs are
    currently set to not be restricted by Void (invisible) walls, while the player is.
    """
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
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




class Wall(pg.sprite.Sprite):
    """
    Walls come in three flavors:
    stops_bullets=True: visible walls
    stops_bullets=False: invisible walls
    stops_bullets="Rift": Rift
    """

    def __init__(self, game, pos, stops_bullets):
        self.game = game
        self._layer = game.settings["layer"]["wall"]
        if stops_bullets == "Rift":
            self.groups = game.walls, game.stops_bullets, game.all_sprites
        elif stops_bullets == True:
            self.groups = game.walls, game.stops_bullets
        else:
            self.groups = game.walls
        self.stops_bullets = stops_bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.rect = pg.Rect(
            0,
            0,
            self.game.settings["gen"]["tilesize"],
            self.game.settings["gen"]["tilesize"],
        )
        self.rect.topleft = self.pos


class Rift(Wall):
    """
    Rifts allow players to move between levels.
    Rifts track distance to player to determine whether
    the player is within distance to use.
    """

    def __init__(self, game, pos):
        Wall.__init__(self, game, pos, "Rift")
        self.game.rift_usable = False
        self.image = self.game.client.data.rift_img

    def check_usable(self):
        self.target_dist = self.game.player.pos - self.pos
        if (
            self.target_dist.length_squared()
            < self.game.settings["lvl"]["rift_usable_distance"] ** 2
        ):
            self.game.rift_usable = True
        else:
            self.game.rift_usable = False

    def update(self):
        self.check_usable()
        if self.game.rift_usable == True:
            keys = pg.key.get_pressed()
            if keys[pg.K_e]:
                # current method of switching levels does not retain player data
                self.game.level("gen", choice(self.game.client.data.biomes))
            if keys[pg.K_r]:
                self.game.level("temple.txt", "void")

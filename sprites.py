# Copyright (c) 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
from os import path
from random import uniform, choice, random
import pytweening as tween

vec = pg.math.Vector2


def collide_hit_rect(one, two):
    """
    Used for hit_rect collision:

    Drawn largely from:
    https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2023
    """
    return one.hit_rect.colliderect(two.rect)


def draw_hp(game, surface, x, y, pct, b_len, b_height, player):
    """
    Used to draw mob and player health bars. 

    Inspired by:
    https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2023
    """
    if pct < 0:
        pct = 0
    if pct > 0.6:
        color = game.settings["colors"]["green"]
    elif pct > 0.3:
        color = game.settings["colors"]["yellow"]
    else:
        color = game.settings["colors"]["red"]
    fill = pct * b_len
    hp_bar = pg.Rect(x, y, fill, b_height)
    pg.draw.rect(surface, color, hp_bar)
    if player:
        outline_rect = pg.Rect(x, y, b_len, b_height)
        pg.draw.rect(surface, game.settings["colors"]["white"], outline_rect, 2)


def draw_score(game):
    """
    Draws the players score and a coin image in the lower right corner of the screen.
    """
    score = game.text_format(
        str(game.player.coins), game.font, 60, game.settings["colors"]["white"]
    )
    game.screen.blit(
        pg.transform.scale(game.item_img["coin"], (92, 92)),
        (game.settings["gen"]["width"] - 100, game.settings["gen"]["height"] - 100),
    )
    score_x = 75 + len(str(game.player.coins)) * 25
    game.screen.blit(
        score,
        (game.settings["gen"]["width"] - score_x, game.settings["gen"]["height"] - 70),
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


class Cursor(pg.sprite.Sprite):
    """
    Cursor class provides an animated cursor target image to 
    replace the default cursor. 
    """

    def __init__(self, game):
        self._layer = game.settings["layer"]["cursor"]
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.cursor_img[0]
        self.rect = self.image.get_rect()
        self.rect.center = pg.mouse.get_pos()
        self.pos = pg.mouse.get_pos()
        self.counter = 0
        self.last = 0

    def update(self):
        now = pg.time.get_ticks()
        if now > self.last + 100:
            self.counter += 1
            self.last = now
        if self.counter > 5:
            self.counter = 0
        self.image = self.game.cursor_img[self.counter]
        self.rect.center = pg.mouse.get_pos()
        self.pos = pg.mouse.get_pos()


class pMove(pg.sprite.Sprite):
    """
    Sprite for player movement is currently separate from the player.
    pMove must be initialized in the same location as the player; layering
    ensures it is rendered underneath the player. 
    Updating pMove cycles the image, providing an animation effect as the player walks. 
    """

    def __init__(self, game, x, y):
        self.game = game
        self._layer = game.settings["layer"]["player_move"]
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images = game.player_img[game.character]["move"]
        self.image = self.images[0]
        self.current = self.image
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.pos = vec(x, y) * game.settings["gen"]["tilesize"]
        self.rot = 0
        self.last = 0
        self.i = 0

    def place(self, x, y):
        self.pos = vec(x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        now = pg.time.get_ticks()
        if self.game.player.vel != [0, 0]:
            self.rot = (self.game.player.vel).angle_to(vec(1, 0)) % 360
            if now - self.last > 100:
                self.last = now
                self.current = self.images[self.i]
                self.i += 1
                if self.i >= len(self.images):
                    self.i = 0
        self.image = pg.transform.rotate(self.current, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.game.player.pos


class Player(pg.sprite.Sprite):
    """
    Player class provides the player sprite and tracks all player data.
    Originally built off code from https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2023,
    but has evolved a lot since. 
    """

    def __init__(self, game, x, y):
        self.game = game
        self._layer = game.settings["layer"]["player"]
        self.groups = game.all_sprites, game.player_sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.stance = "magic"
        self.image = game.player_img[game.character][self.stance]
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.hit_rect = pg.Rect(game.settings["player"]["hit_rect"])
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.max_hp = game.settings["player"]["hp"]
        self.hp = game.settings["player"]["hp"]
        self.speed = (
            game.settings["gen"]["tilesize"] * game.settings["player"]["speed_mult"]
        )
        self.coins = 0

    def place(self, x, y):
        self.pos = vec(x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()
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
            if now - self.last_shot > self.game.settings["weapon"]["vbullet"]["rate"]:
                self.last_shot = now
                angle = (self.game.cursor.pos - self.pos).angle_to(vec(1, 0))
                dir = vec(1, 0).rotate(-angle)
                pos = self.pos + vec(
                    self.game.settings["player"]["hand_offset"]
                ).rotate(-self.rot)
                Bullet(self.game, pos, dir, self.rot)
                if self.game.settings["gen"]["sound"] == "on" and random() < 0.75:
                    self.game.sounds["wave01"].play()
                Weapon_VFX(
                    self.game,
                    self.pos
                    + vec(self.game.settings["player"]["hand_offset"]).rotate(
                        -self.rot
                    ),
                )

        if self.vel.x != 0 and self.vel.y != 0:
            # correct diagonal movement to be same speed
            # multiply by 1/sqrt(2)
            self.vel *= 0.70701

    def update(self):
        self.get_keys()
        self.rot = (self.game.cursor.pos - self.pos).angle_to(vec(1, 0)) % 360
        self.image = pg.transform.rotate(
            self.game.player_img[self.game.character][self.stance], self.rot
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, "y")
        self.rect.center = self.hit_rect.center

    def add_hp(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp


class Bullet(pg.sprite.Sprite):
    """
    Bullet class provides bullet sprites with image, velocity and lifetime tracking. 
    Originally built off code from https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2023.
    """

    def __init__(self, game, pos, dir, rot):
        self.game = game
        self._layer = game.settings["layer"]["bullet"]
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rot = rot
        self.image = pg.transform.rotate(game.vbullet_img, self.rot + 90)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(
            -game.settings["weapon"]["vbullet"]["spread"],
            game.settings["weapon"]["vbullet"]["spread"],
        )
        self.vel = dir.rotate(spread) * game.settings["weapon"]["vbullet"]["speed"]
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if (
            pg.sprite.spritecollideany(self, self.game.stops_bullets)
            or pg.time.get_ticks() - self.spawn_time
            > self.game.settings["weapon"]["vbullet"]["life"]
        ):
            self.kill()


class Mob(pg.sprite.Sprite):
    """
    Mob class provides mob sprites and tracks mob instance data. 
    Originally built off code from https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2023.
    """

    def __init__(self, game, kind, x, y):
        self.game = game
        self.kind = kind
        self._layer = game.settings["layer"]["mob"]
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.mob_img[kind].copy()
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.hit_rect = pg.Rect(
            0,
            0,
            game.settings["gen"]["tilesize"] / 2,
            game.settings["gen"]["tilesize"] / 2,
        )
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * self.game.settings["gen"]["tilesize"]
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.hp = game.settings["mob"][kind]["hp"]
        self.max_hp = game.settings["mob"][kind]["hp"]
        self.speed = game.settings["gen"]["tilesize"] * choice(
            game.settings["mob"][kind]["speed"]
        )
        self.triggered = False
        self.last_hit = 0
        self.items = [("redpotion", "hp"), ("coin", "gp")]

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < self.game.settings["gen"]["tilesize"] * 2:
                    self.acc += dist.normalize()

    def update(self):
        self.target_dist = self.game.player.pos - self.pos
        self.rot = self.target_dist.angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img[self.kind], self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        if (
            self.triggered == False
            and self.target_dist.length_squared()
            < self.game.settings["mob"][self.kind]["player_radius"] ** 2
        ):
            self.triggered = True
            if self.game.settings["gen"]["sound"] == "on":
                self.game.sounds["growl01"].play()
        if self.triggered:
            # self.acc = vec(MOB['THRALL_SPEED'][0],0).rotate(-self.rot)
            if self.game.settings["gen"]["sound"] == "on" and random() < 0.0015:
                self.game.sounds["growl01"].play()
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            try:
                self.acc.scale_to_length(self.speed)
            except Exception as e:
                print("{}".format(e))
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            # Equations of motion
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 1.025
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, "x")
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, "y")
            self.rect.center = self.hit_rect.center
        if self.hp <= 0:
            Grave(self.game, self.kind, self.pos, self.rot)
            if random() < self.game.settings["mob"][self.kind]["drop_chance"]:
                item = choice(self.items)
                Item(self.game, self.pos, item[0], item[1])
            self.game.mob_count -= 1
            self.kill()


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
        self.image = self.game.rift_img

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
                self.game.level("gen", choice(self.game.biomes))
            if keys[pg.K_r]:
                self.game.level("temple.txt", "void")


class Grave(pg.sprite.Sprite):
    """
    Graves are left behind when mobs are killed,
    with rotation matched to the mob rotation on death. 
    Grave images are a random choice from graves available
    for that enemy kind. 
    """

    def __init__(self, game, kind, pos, rot):
        self.game = game
        self._layer = game.settings["layer"]["grave"]
        self.groups = game.all_sprites, game.graves
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.image = pg.transform.rotate(
            pg.transform.scale(
                choice(game.grave_img[kind]),
                (
                    self.game.settings["gen"]["tilesize"],
                    self.game.settings["gen"]["tilesize"],
                ),
            ),
            rot,
        )
        self.rect = self.image.get_rect()
        self.rect.center = pos


class Weapon_VFX(pg.sprite.Sprite):
    """
    Weapon_VFX appear when the player is shooting.
    Cycling between available img options provides
    animation effect.

    Drawn largely from:
    https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2023
    """

    def __init__(self, game, pos):
        self._layer = game.settings["layer"]["vfx"]
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(
            choice(game.weapon_vfx),
            (
                self.game.settings["gen"]["tilesize"],
                self.game.settings["gen"]["tilesize"],
            ),
        )
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if (
            pg.time.get_ticks() - self.spawn_time
            > self.game.settings["weapon"]["vbullet"]["fx_life"]
        ):
            self.kill()


class Item(pg.sprite.Sprite):
    """
    Item class is used to place items on the map. 
    Items use tween animations from the pytweening library. 

    Drawn largely from:
    https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2023
    """

    def __init__(self, game, pos, img, kind):
        self.game = game
        self._layer = game.settings["layer"]["item"]
        self.bob_range = game.settings["items"]["bob_range"]
        self.bob_speed = game.settings["items"]["bob_speed"]
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game.item_img[img]
        self.kind = kind
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # item bobbing motion
        offset = self.bob_range * (self.tween(self.step / self.bob_range) - 0.5)
        self.rect.centery = self.pos[1] + offset * self.dir
        self.step += self.bob_speed
        if self.step > self.bob_range:
            self.step = 0
            self.dir *= -1

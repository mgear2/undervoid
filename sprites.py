# Copyright (c) 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Building off example code from
# https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap

import pygame as pg
from settings import *
from os import path
from random import uniform, choice, random
from tilemap import collide_hit_rect
import pytweening as tween
vec = pg.math.Vector2

def draw_hp(surface, x, y, pct, b_len, b_height, player):
    if pct < 0:
        pct = 0
    if pct > 0.6:
        color = COLORS['GREEN']
    elif pct > 0.3:
        color = COLORS['YELLOW']
    else:
        color = COLORS['RED']
    fill = pct * b_len
    hp_bar = pg.Rect(x, y, fill, b_height)
    pg.draw.rect(surface, color, hp_bar)
    if player:
        outline_rect = pg.Rect(x, y, b_len, b_height)
        pg.draw.rect(surface, COLORS['WHITE'], outline_rect, 2)

def collide_with_walls(sprite, group, dir):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits: 
        if dir == 'x':
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2 
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
        if dir == 'y':
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Cursor(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = LAYER['CURSOR']
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.cursor_img[0]
        self.rect = self.image.get_rect()
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
    def __init__(self, game, x, y):
        self._layer = LAYER['PLAYER_MOVE']
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = self.game.pmove_img
        self.image = self.images[0]
        self.current = self.image
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.pos = vec(x, y) * GEN['TILESIZE']
        self.rot = 0
        self.last = 0
        self.i = 0

    def update(self):
        now = pg.time.get_ticks()
        if self.game.player.vel != [0, 0]:
            self.rot = (self.game.player.vel).angle_to(vec(1,0)) % 360
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
    def __init__(self, game, x, y):
        self._layer = LAYER['PLAYER']
        self.groups = game.all_sprites, game.player_sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.hit_rect = PLAYER['HIT_RECT']
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * GEN['TILESIZE']
        self.rot = 0
        self.last_shot = 0
        self.hp = PLAYER['HP']

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER['SPEED']
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER['SPEED']
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER['SPEED']
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER['SPEED']
        if keys[pg.K_SPACE] or mouse[0]:
            now = pg.time.get_ticks()
            if now - self.last_shot > WEAPON['VBULLET_RATE']:
                self.last_shot = now
                angle = (self.game.cursor.pos - self.pos).angle_to(vec(1, 0))
                dir = vec(1, 0).rotate(-angle)
                pos = self.pos + PLAYER['HAND_OFFSET'].rotate(-self.rot)
                Bullet(self.game, pos, dir, self.rot)
                if random() < 0.75:
                    self.game.sounds['wave01'].play()
                Weapon_VFX(self.game, self.pos + PLAYER['HAND_OFFSET'].rotate(-self.rot))

        if self.vel.x != 0 and self.vel.y != 0:
            # correct diagonal movement to be same speed
            # multiply by 1/sqrt(2)
            self.vel *= 0.70701

    def update(self):
        self.get_keys()
        self.rot = (self.game.cursor.pos - self.pos).angle_to(vec(1,0)) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def add_hp(self, amount):
        self.hp += amount
        if self.hp > PLAYER['HP']:
            self.hp = PLAYER['HP']

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, rot):
        self._layer = LAYER['BULLET']
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rot = rot
        self.image = pg.transform.rotate(game.vbullet_img, self.rot + 90)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-WEAPON['VSPREAD'], WEAPON['VSPREAD'])
        self.vel = dir.rotate(spread) * WEAPON['VBULLET_SPEED']
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if (pg.sprite.spritecollideany(self, self.game.stops_bullets)
                or pg.time.get_ticks() - self.spawn_time > WEAPON['VBULLET_LIFETIME']):
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = LAYER['MOB']
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.thrall_img
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.hit_rect = MOB['THRALL_HIT_RECT'].copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * GEN['TILESIZE']
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.hp = MOB['THRALL_HP']
        self.max_hp = MOB['THRALL_HP']
        self.speed = GEN['TILESIZE'] * choice(MOB['THRALL_SPEED'])
        self.triggered = False
        self.last_hit = 0

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < MOB['THRALL_RADIUS']:
                    self.acc += dist.normalize()

    def update(self):
        self.target_dist = self.game.player.pos - self.pos
        self.rot = self.target_dist.angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.thrall_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        if self.triggered == False and self.target_dist.length_squared() < MOB['DETECT_RADIUS'] ** 2:    
            self.triggered = True
            self.game.sounds['growl01'].play()
        if self.triggered:
            #self.acc = vec(MOB['THRALL_SPEED'][0],0).rotate(-self.rot)
            if random() < 0.0015:
                self.game.sounds['growl01'].play()
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            try:
                self.acc.scale_to_length(self.speed)
            except Exception as e:
                print("{}".format(e))
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            # Equations of motion
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 1.005
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.hp <= 0: 
            Grave(self.game, self.pos, self.rot)
            if random() < MOB['DROP_CHANCE']:
                Item(self.game, self.pos, 'POTION_1', 'hp')
            self.kill()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, pos, stops_bullets):
        self._layer = LAYER['WALL']
        if stops_bullets:
            self.groups = game.walls, game.stops_bullets
        else:
            self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = pos
        self.rect = pg.Rect(0, 0, GEN['TILESIZE'], GEN['TILESIZE'])
        self.rect.topleft = self.pos

class Grave(pg.sprite.Sprite):
    def __init__(self, game, pos, rot):
        self._layer = LAYER['GRAVE']
        self.groups = game.all_sprites, game.graves
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.image = pg.transform.rotate(pg.transform.scale(choice(game.thrall_grave), (GEN['TILESIZE'], GEN['TILESIZE'])), rot)
        self.rect = self.image.get_rect()
        self.rect.center = pos

class Weapon_VFX(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = LAYER['VFX']
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(choice(game.weapon_vfx), (WEAPON['VDUST_SIZE'], WEAPON['VDUST_SIZE']))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > WEAPON['VDUST_LIFETIME']:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, img, kind):
        self._layer = LAYER['ITEM']
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
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
        offset = ITEMS['BOB_RANGE'] * (self.tween(self.step / ITEMS['BOB_RANGE']) - 0.5) 
        self.rect.centery = self.pos[1] + offset * self.dir
        self.step += ITEMS['BOB_SPEED']
        if self.step > ITEMS['BOB_RANGE']:
            self.step = 0
            self.dir *= -1
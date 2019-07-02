# Copyright (c) 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Building off example code from
# https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap

import pygame as pg
from settings import *
from os import path
from random import uniform
from tilemap import collide_hit_rect
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if dir == 'x':
            if hits:
                if hits[0].rect.centerx > sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
                if hits[0].rect.centerx < sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2 
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
        if dir == 'y':
            if hits:
                if hits[0].rect.centery > sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
                if hits[0].rect.centery < sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y

class Cursor(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.cursor_img
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.center = pg.mouse.get_pos()
        self.pos = pg.mouse.get_pos()

    def update(self):
        self.rect.center = pg.mouse.get_pos()
        self.pos = pg.mouse.get_pos()

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.player_sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_SETTINGS['HIT_RECT']
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * GEN_SETTINGS['TILESIZE']
        self.rot = 0
        self.last_shot = 0
        self.hp = PLAYER_SETTINGS['HP']

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        mouse = pg.mouse.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SETTINGS['SPEED']
            #self.rot_speed = PLAYER_SETTINGS['ROT_SPEED']
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SETTINGS['SPEED']
            #self.rot_speed = -PLAYER_SETTINGS['ROT_SPEED']
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SETTINGS['SPEED']
            #self.vel = vec(PLAYER_SETTINGS['SPEED'], 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SETTINGS['SPEED']
            #self.vel = vec(-PLAYER_SETTINGS['SPEED'], 0).rotate(-self.rot)
        if keys[pg.K_SPACE] or mouse[0]:
            now = pg.time.get_ticks()
            if now - self.last_shot > WEAPON_SETTINGS['VBULLET_RATE']:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + PLAYER_SETTINGS['HAND_OFFSET'].rotate(-self.rot)
                Bullet(self.game, pos, dir)

        #if self.vel.x != 0 and self.vel.y != 0:
            # correct diagonal movement to be same speed
            # multiply by 1/sqrt(2)
            # need to revisit this
        #    self.vel *= 0.70701

    def update(self):
        self.get_keys()
        self.rot = (self.game.cursor.pos - self.pos).angle_to(vec(1,0))
        # self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.vbullet_img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-WEAPON_SETTINGS['VSPREAD'], WEAPON_SETTINGS['VSPREAD'])
        self.vel = dir.rotate(spread) * WEAPON_SETTINGS['VBULLET_SPEED']
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if (pg.sprite.spritecollideany(self, self.game.walls)
                or pg.time.get_ticks() - self.spawn_time > WEAPON_SETTINGS['VBULLET_LIFETIME']):
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.thrall_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_SETTINGS['THRALL_HIT_RECT'].copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * GEN_SETTINGS['TILESIZE']
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.hp = MOB_SETTINGS['THRALL_HP']

    def update(self):
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.image = pg.transform.rotate(self.game.thrall_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(MOB_SETTINGS['THRALL_SPEED'],0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        # Equations of motion
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.hp <= 0: 
            self.kill()
        
    def draw_hp(self):
        if self.hp > 60:
            bar_color = COLORS['GREEN']
        elif self.hp > 30:
            bar_color = COLORS['YELLOW']
        else:
            bar_color = COLORS['RED']
        width = int(self.rect.width * self.hp / MOB_SETTINGS['THRALL_HP'])
        self.hp_bar = pg.Rect(0, 0, width, 7)
        if self.hp < MOB_SETTINGS['THRALL_HP']:
            pg.draw.rect(self.image, bar_color, self.hp_bar)

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(path.join(self.game.img_folder, IMAGES['WALL_IMG']))
        self.image = pg.transform.scale(self.image, (GEN_SETTINGS['TILESIZE'], GEN_SETTINGS['TILESIZE']))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * GEN_SETTINGS['TILESIZE']
        self.rect.y = y * GEN_SETTINGS['TILESIZE']

class Floor(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(path.join(self.game.img_folder, IMAGES['FLOOR_IMG']))
        self.image = pg.transform.scale(self.image, (GEN_SETTINGS['TILESIZE'], GEN_SETTINGS['TILESIZE']))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * GEN_SETTINGS['TILESIZE']
        self.rect.y = y * GEN_SETTINGS['TILESIZE']
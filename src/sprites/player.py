import pygame as pg
from random import uniform, choice, random
from src.sprites.sprites import *
from src.sprites.bullet import Bullet
from src.sprites.weapon_vfx import Weapon_VFX

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    """
    Player class provides the player sprite and tracks all player data.
    """

    def __init__(self, settings, all_sprites, player_sprite, player_img, x, y):
        # self.game = game
        self.settings = settings
        self._layer = settings["layer"]["player"]
        self.groups = all_sprites, player_sprite
        pg.sprite.Sprite.__init__(self, self.groups)
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

    def place(self, x, y):
        self.pos = vec(x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def get_keys(
        self,
        game_cursor_pos,
        game_sound,
        bullets,
        game_client_data_bullet_img,
        stops_bullets,
        weapon_vfx_sprite,
        game_client_data_weaponvfx,
    ):
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
            if now - self.last_shot > self.settings["weapon"]["vbullet"]["rate"]:
                self.last_shot = now
                angle = (game_cursor_pos - self.pos).angle_to(vec(1, 0))
                dir = vec(1, 0).rotate(-angle)
                pos = self.pos + vec(self.settings["player"]["hand_offset"]).rotate(
                    -self.rot
                )
                Bullet(
                    self.settings,
                    self.groups[0],
                    bullets,
                    game_client_data_bullet_img,
                    stops_bullets,
                    pos,
                    dir,
                    self.rot,
                )
                if self.settings["gen"]["sound"] == "on" and random() < 0.75:
                    game_sound.play()
                Weapon_VFX(
                    self.settings,
                    self.groups[0],
                    weapon_vfx_sprite,
                    game_client_data_weaponvfx,
                    self.pos
                    + vec(self.settings["player"]["hand_offset"]).rotate(-self.rot),
                )

        if self.vel.x != 0 and self.vel.y != 0:
            # correct diagonal movement to be same speed
            # multiply by 1/sqrt(2)
            self.vel *= 0.70701

    def update(
        self,
        game_cursor_pos,
        game_sound,
        game_client_data_player_img,
        game_client_dt,
        game_walls,
        bullets,
        game_client_data_bullet_img,
        stops_bullets,
        weapon_vfx_sprite,
        game_client_data_weaponvfx,
    ):
        self.get_keys(
            game_cursor_pos,
            game_sound,
            bullets,
            game_client_data_bullet_img,
            stops_bullets,
            weapon_vfx_sprite,
            game_client_data_weaponvfx,
        )
        self.rot = (game_cursor_pos - self.pos).angle_to(vec(1, 0)) % 360
        self.image = pg.transform.rotate(
            game_client_data_player_img,
            self.rot,
        )
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * game_client_dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, game_walls, "x")
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, game_walls, "y")
        self.rect.center = self.hit_rect.center

    def add_hp(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

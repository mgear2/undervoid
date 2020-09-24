import pygame as pg
from random import choice


class Weapon_VFX(pg.sprite.Sprite):
    """
    Weapon_VFX appear when the player is shooting.
    Cycling between available img options provides
    animation effect.
    """

    def __init__(
        self, settings, all_sprites, weaponvfx_sprite, game_client_data_weaponvfx, pos
    ):
        self.settings = settings
        self._layer = self.settings["layer"]["vfx"]
        self.groups = all_sprites, weaponvfx_sprite
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = pg.transform.scale(
            choice(game_client_data_weaponvfx),
            (
                self.settings["gen"]["tilesize"],
                self.settings["gen"]["tilesize"],
            ),
        )
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if (
            pg.time.get_ticks() - self.spawn_time
            > self.settings["weapon"]["vbullet"]["fx_life"]
        ):
            self.kill()

import pygame as pg
from random import choice

class Grave(pg.sprite.Sprite):
    """
    Graves are left behind when mobs are killed,
    with rotation matched to the mob rotation on death.
    Grave images are a random choice from graves available
    for that enemy kind.
    """

    def __init__(self, settings, all_sprites, grave_group, game_client_data_mob_img, kind, pos, rot):
        self.settings = settings
        self._layer = self.settings["layer"]["grave"]
        self.groups = all_sprites, grave_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.image = pg.transform.rotate(
            pg.transform.scale(
                choice(game_client_data_mob_img["grave"][kind]),
                (
                    self.settings["gen"]["tilesize"],
                    self.settings["gen"]["tilesize"],
                ),
            ),
            rot,
        )
        self.rect = self.image.get_rect()
        self.rect.center = pos
import pygame as pg
import pytweening as tween



class Item(pg.sprite.Sprite):
    """
    Item class is used to place items on the map.
    Items use tween animations from the pytweening library.
    """

    def __init__(self, settings, all_sprites, item_group, game_client_data_item_img, pos, img, kind):
        self.settings = settings
        self._layer = self.settings["layer"]["item"]
        self.bob_range = self.settings["items"]["bob_range"]
        self.bob_speed = self.settings["items"]["bob_speed"]
        self.groups = all_sprites, item_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = game_client_data_item_img[img]
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
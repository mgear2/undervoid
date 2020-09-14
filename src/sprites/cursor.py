import pygame as pg

class Cursor(pg.sprite.Sprite):
    """
    Cursor class provides an animated cursor target image to 
    replace the default cursor. 
    """

    def __init__(self, settings, all_sprites, cursor_sprite, cursor_img):
        self._layer = settings["layer"]["cursor"]
        self.groups = all_sprites, cursor_sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        # self.game = game
        self.cursor_img = cursor_img
        self.image = cursor_img[0]
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
        self.image = self.cursor_img[self.counter]
        self.rect.center = pg.mouse.get_pos()
        self.pos = pg.mouse.get_pos()

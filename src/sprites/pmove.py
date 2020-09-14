import pygame as pg

vec = pg.math.Vector2


class pMove(pg.sprite.Sprite):
    """
    Sprite for player movement is currently separate from the player.
    pMove must be initialized in the same location as the player; layering
    ensures it is rendered underneath the player. 
    Updating pMove cycles the image, providing an animation effect as the player walks. 
    """

    def __init__(self, settings, all_sprites, pmove_group, player_img, x, y):
        # self.game = game
        self._layer = settings["layer"]["player_move"]
        self.groups = all_sprites, pmove_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.images = player_img
        self.image = self.images[0]
        self.current = self.image
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.pos = vec(x, y) * settings["gen"]["tilesize"]
        self.rot = 0
        self.last = 0
        self.i = 0

    def place(self, x, y):
        self.pos = vec(x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, velocity: [int], player_position):
        now = pg.time.get_ticks()
        if velocity != [0, 0]:
            self.rot = (velocity).angle_to(vec(1, 0)) % 360
            if now - self.last > 100:
                self.last = now
                self.current = self.images[self.i]
                self.i += 1
                if self.i >= len(self.images):
                    self.i = 0
        self.image = pg.transform.rotate(self.current, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = player_position
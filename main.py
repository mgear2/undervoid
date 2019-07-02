# Copyright (c) 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Building off example code from
# https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import Map
from tilemap import Camera

def draw_player_hp(surface, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 200
    BAR_HEIGHT = 15
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        color = COLORS['GREEN']
    elif pct > 0.3:
        color = COLORS['YELLOW']
    else:
        color = COLORS['RED']
    pg.draw.rect(surface, color, fill_rect)
    pg.draw.rect(surface, COLORS['WHITE'], outline_rect, 2)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((GEN_SETTINGS['WIDTH'], GEN_SETTINGS['HEIGHT']))
        pg.display.set_caption(GEN_SETTINGS['TITLE'])
        self.clock = pg.time.Clock()
        pg.key.set_repeat(100, 100)
        self.load_data()

    def load_data(self):
        self.game_folder = path.dirname(__file__)

        self.data_folder = path.join(self.game_folder, 'data')
        self.img_folder = path.join(self.data_folder, 'img')
        self.maps_folder = path.join(self.data_folder, 'maps')
        self.music_folder = path.join(self.data_folder, 'music')

        self.undervoid_icon = pg.image.load(path.join(self.img_folder, IMAGES['ICON_IMG'])).convert_alpha()
        self.undervoid_icon = pg.transform.scale(self.undervoid_icon, (64, 64))
        self.player_img = pg.image.load(path.join(self.img_folder, IMAGES['PLAYER_IMG'])).convert_alpha()
        self.vbullet_img = pg.image.load(path.join(self.img_folder, IMAGES['VBULLET_IMG'])).convert_alpha()
        #self.vbullet_img = pg.transform.scale(self.vbullet_img, (GEN_SETTINGS['TILESIZE'], GEN_SETTINGS['TILESIZE']))
        self.thrall_img = pg.image.load(path.join(self.img_folder, IMAGES['THRALL_IMG'])).convert_alpha()
        self.floor_img = pg.image.load(path.join(self.img_folder, IMAGES['FLOOR_IMG_6'])).convert_alpha()
        #self.player_img = pg.transform.scale(self.player_img, (TILESIZE, TILESIZE))
        #self.cursor_img = pg.image.load(path.join(self.img_folder, CURSOR_IMG)).convert_alpha()
        #pg.mouse.set_visible(False)
        # https://stackoverflow.com/questions/43845800/how-do-i-add-background-music-to-my-python-game#43845914
        pg.display.set_icon(self.undervoid_icon)
        #pg.mixer.init()
        #pg.mixer.music.load(path.join(self.music_folder, MUSIC['leavinghome']))
        #pg.mixer.music.play(-1, 0.0)
        self.map = Map(self, path.join(self.maps_folder, 'map1.txt'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                #if tile == '.' or tile == 'P':
                #    Floor(self, col, row)
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    #Floor(self, col, row)
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
        #self.cursor = Cursor(self)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(GEN_SETTINGS['FPS']) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.hp -= MOB_SETTINGS['THRALL_DMG']
            hit.vel = vec(0, 0)
            if self.player.hp <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_SETTINGS['THRALL_KB'], 0).rotate(-hits[0].rot)
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.hp -= WEAPON_SETTINGS['VDMG']
            hit.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, GEN_SETTINGS['WIDTH'], GEN_SETTINGS['TILESIZE']):
            pg.draw.line(self.screen, COLORS['LIGHTGREY'], (x, 0), (x, GEN_SETTINGS['HEIGHT']))
        for y in range(0, GEN_SETTINGS['HEIGHT'], GEN_SETTINGS['TILESIZE']):
            pg.draw.line(self.screen, COLORS['LIGHTGREY'], (0, y), (GEN_SETTINGS['WIDTH'], y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(GEN_SETTINGS['BGCOLOR'])
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_hp()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        draw_player_hp(self.screen, 10, GEN_SETTINGS['HEIGHT'] - 30, self.player.hp / PLAYER_SETTINGS['HP'])
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
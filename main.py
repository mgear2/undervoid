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

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((GEN['WIDTH'], GEN['HEIGHT']))
        pg.display.set_caption(GEN['TITLE'])
        self.clock = pg.time.Clock()
        pg.key.set_repeat(100, 100)
        self.load_data()

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.data_folder = path.join(self.game_folder, 'data')
        self.img_folder = path.join(self.data_folder, 'img')
        self.maps_folder = path.join(self.data_folder, 'maps')
        self.music_folder = path.join(self.data_folder, 'music')
        self.sound_folder = path.join(self.data_folder, 'sounds')

        self.undervoid_icon = pg.image.load(path.join(self.img_folder, IMG['ICON'])).convert_alpha()
        self.undervoid_icon = pg.transform.scale(self.undervoid_icon, (64, 64))
        #self.player_img = pg.image.load(path.join(self.img_folder, IMG['VOIDWALKER'])).convert_alpha()
        self.vbullet_img = pg.image.load(path.join(self.img_folder, IMG['VBULLET'])).convert_alpha()
        self.vbullet_img = pg.transform.scale(self.vbullet_img, (64, 64))
        self.thrall_img = pg.image.load(path.join(self.img_folder, IMG['THRALL'])).convert_alpha()
        self.thrall_img = pg.transform.scale(self.thrall_img, (GEN['TILESIZE'], GEN['TILESIZE']))
        self.wall_img = pg.image.load(path.join(self.img_folder, IMG['VOIDWALL']))
        self.wall_img = pg.transform.scale(self.wall_img, (GEN['TILESIZE'], GEN['TILESIZE']))

        self.player_img_list = []
        self.pmove_img = []
        self.cursor_img = []
        self.weapon_vfx = []
        self.item_img = {}
        self.floor_img = []
        self.thrall_grave = []

        self.item_img['POTION_1'] = pg.transform.scale(pg.image.load(path.join(self.img_folder, IMG['POTION_1'])).convert_alpha(), (48, 48))

        for img in IMG['VOIDWALKER']:
            self.player_img_list.append(pg.image.load(path.join(self.img_folder, img)).convert_alpha())
        self.player_img = pg.transform.scale(self.player_img_list[0], (GEN['PLAYERSIZE'], GEN['PLAYERSIZE']))
        for img in IMG['VOIDWALKER_MOVE']:
            self.pmove_img.append(pg.transform.scale((pg.image.load(path.join(self.img_folder, img)).convert_alpha()), (GEN['PLAYERSIZE'] + 16, GEN['PLAYERSIZE'] + 16)))
        for img in IMG['D_FLOOR']:
            self.floor_img.append(pg.image.load(path.join(self.img_folder, img)).convert_alpha())
        for img in IMG['CURSOR']:
            self.cursor_img.append(pg.image.load(path.join(self.img_folder, img)).convert_alpha())
        for img in WEAPON['VBULLET_VFX']:
            self.weapon_vfx.append(pg.image.load(path.join(self.img_folder, img)).convert_alpha())
        for img in IMG['THRALL_GRAVE']:
            self.thrall_grave.append(pg.image.load(path.join(self.img_folder, img)).convert_alpha())

        self.sounds = {}
        for sound in SOUNDS:
            self.sounds[sound] = pg.mixer.Sound(path.join(self.sound_folder, SOUNDS[sound]))
        pg.mixer.init()
        pg.mixer.music.load(path.join(self.music_folder, MUSIC['leavinghome']))
        pg.mixer.music.play(-1, 0.0)

        pg.mouse.set_visible(False)
        pg.display.set_icon(self.undervoid_icon)

        self.map = Map(self, path.join(self.maps_folder, 'map3.txt'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.graves = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        self.cursor_sprite = pg.sprite.Group()
        self.cursor = Cursor(self)

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1' or tile == '0':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                    self.pmove = pMove(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'p':
                    Item(self, col, row, 'POTION_1', 'hp')

        self.camera = Camera(self.map.width, self.map.height, self.cursor)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(GEN['FPS']) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False, collide_hit_rect)
        for hit in hits:
            if hit.kind == 'hp' and self.player.hp < PLAYER['HP']:
                hit.kill()
                self.sounds['treasure02'].play()
                self.player.add_hp(ITEMS['POTION_1_HP'])
        # mobs hitting player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.hp -= MOB['THRALL_DMG']
            hit.vel = vec(0, 0)
            if self.player.hp <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB['THRALL_KB'], 0).rotate(-hits[0].rot)
        # bullets hitting mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.hp -= WEAPON['VDMG']
            #hit.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, GEN['WIDTH'], GEN['TILESIZE']):
            pg.draw.line(self.screen, COLORS['LIGHTGREY'], (x, 0), (x, GEN['HEIGHT']))
        for y in range(0, GEN['HEIGHT'], GEN['TILESIZE']):
            pg.draw.line(self.screen, COLORS['LIGHTGREY'], (0, y), (GEN['WIDTH'], y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(GEN['BGCOLOR'])
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob) and sprite.hp < sprite.max_hp:
                draw_hp(sprite.image, 0, 0, sprite.hp / sprite.max_hp, GEN['TILESIZE'], 7, False)
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        draw_hp(self.screen, 10, GEN['HEIGHT'] - 30, self.player.hp / PLAYER['HP'], 200, 15, True)
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

if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while True:
        g.new()
        g.run()
        g.show_go_screen()
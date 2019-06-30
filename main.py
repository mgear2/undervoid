# Copyright © 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Example code drawn from
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
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(100, 100)
        self.load_data()

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.data_folder = path.join(self.game_folder, 'data')
        self.img_folder = path.join(self.data_folder, 'img')
        self.maps_folder = path.join(self.data_folder, 'maps')
        self.music_folder = path.join(self.data_folder, 'music')
        self.undervoid_icon = pg.image.load(path.join(self.img_folder, 'voidbullet.png')).convert_alpha()
        self.undervoid_icon = pg.transform.scale(self.undervoid_icon, (64, 64))
        pg.display.set_icon(self.undervoid_icon)
        # https://stackoverflow.com/questions/43845800/how-do-i-add-background-music-to-my-python-game#43845914
        pg.mixer.init()
        pg.mixer.music.load(path.join(self.music_folder, 'Leaving Home.mp3'))
        pg.mixer.music.play(-1, 0.0)
        self.map = Map(path.join(self.maps_folder, 'map1.txt'))

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
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
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
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
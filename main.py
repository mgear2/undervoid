# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import ruamel.yaml
import pygame as pg
import sys
from src.sprites.sprites import *
from os import path, environ
from src.game import Game
from src.sprites.mob import Mob
from src.loader import Loader
from src.menu import Menu

yaml = ruamel.yaml.YAML()


class Client:
    """
    Client Class
    """

    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.game, self.player, self.character = None, None, None
        with open("settings.yaml") as f:
            self.settings = yaml.load(f)
            f.close()
        self.init_game_window()
        pg.display.set_caption(self.settings["gen"]["title"])
        self.clock = pg.time.Clock()
        pg.key.set_repeat(100, 100)
        self.data = Loader(self.settings)
        self.data.build_path()
        self.data.load_data()

        pg.mouse.set_visible(False)
        pg.display.set_icon(self.data.undervoid_icon)

    def init_game_window(self):
        """
        Initializes a centered game window either with windowed resolution or fullscreen.
        """
        environ["SDL_VIDEO_CENTERED"] = "1"
        if self.settings["gen"]["fullscreen"] == "on":
            self.settings["gen"]["width"], self.settings["gen"]["height"] = (
                pg.display.Info().current_w,
                pg.display.Info().current_h,
            )
            self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        else:
            self.settings["gen"]["width"] = self.settings["gen"]["winres"]["width"]
            self.settings["gen"]["height"] = self.settings["gen"]["winres"]["height"]
            self.screen = pg.display.set_mode(
                (self.settings["gen"]["width"], self.settings["gen"]["height"])
            )

    def draw(self):
        """
        Draws the map and all sprites.
        Draws Player health and gold coins.
        """
        pg.display.set_caption("Undervoid")
        self.screen.fill(self.game.bg_color)
        self.screen.blit(
            self.game.map_img, self.game.camera.apply_rect(self.game.map_rect)
        )
        # self.draw_grid()
        for sprite in self.game.all_sprites:
            if isinstance(sprite, Mob) and sprite.hp < sprite.max_hp:
                draw_hp(
                    self,
                    sprite.image,
                    0,
                    0,
                    sprite.hp / sprite.max_hp,
                    self.settings["gen"]["tilesize"],
                    int(self.settings["gen"]["tilesize"] / 10),
                    False,
                )
            self.screen.blit(sprite.image, self.game.camera.apply(sprite))
        draw_hp(
            self,
            self.screen,
            10,
            self.settings["gen"]["height"] - 30,
            self.player.hp / self.player.max_hp,
            200,
            15,
            True,
        )
        draw_score(self)
        if self.settings["gen"]["displayfps"] == "on":
            draw_fps(self)
        pg.display.flip()

    def events(self):
        """
        Checks for key/mouse presses.
        Checks if the user is quitting the game.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if self.menu.inmenu:
                    self.menu.menu_event(event)

    # Text Renderer https://www.sourcecodester.com/tutorials/python/11784/python-pygame-simple-main-menu-selection.html
    def text_format(self, message: str, textFont: str, textSize: int, textColor=[0,0,0]) -> pg.font.Font:
        """
        Returns a pygame text ready to be drawn to screen.
        """
        newFont = pg.font.SysFont(textFont, textSize)
        newText = newFont.render(message, 0, textColor)

        return newText

    def show_start_screen(self):
        """
        Initializes the menus, music, and starts menu loop.
        """
        self.font = "franklingothic"
        pg.mixer.music.load(
            path.join(self.data.music_folder, self.settings["music"]["voidwalk"])
        )
        if self.settings["gen"]["music"] == "on":
            pg.mixer.music.play(-1, 0.0)
        self.menu = Menu(self)
        self.menu.update_settings()
        self.menu.run(self.menu.menu_main)

    def show_go_screen(self):
        """
        This method is used upon player death to restart at the main menu.
        """
        self.show_start_screen()
        g = Game(c)
        self.run(g)

    def run(self, game: Game):
        """
        Game loop; ticks the clock, checks for events, updates game state, draws game state
        """
        self.game = game
        if self.settings["gen"]["music"] == "on":
            pg.mixer.music.load(
                path.join(self.data.music_folder, self.settings["music"]["leavinghome"])
            )
            pg.mixer.music.play(-1, 0.0)

        self.playing = True
        while self.playing:
            # tick_busy_loop() uses more cpu but is more accurate
            self.dt = self.clock.tick_busy_loop(self.settings["gen"]["fps"]) / 1000
            self.events()
            game.update()
            if self.player.hp <= 0:
                self.playing = False
            self.draw()

    def quit(self):
        """
        Quits pygame and exits the program
        """
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    c = Client()
    c.show_start_screen()
    g = Game(c)
    while True:
        c.run(g)
        c.show_go_screen()

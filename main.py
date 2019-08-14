# Copyright (c) 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Building off example code from
# https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap

import pygame as pg
import sys
import ruamel.yaml
from os import path, environ
from sprites import *
from tilemap import Camera, Spawner, Forge
from random import random, randint

yaml = ruamel.yaml.YAML()


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        with open("settings.yaml") as f:
            self.settings = yaml.load(f)
            f.close()
        self.init_game_window()
        pg.display.set_caption(self.settings["gen"]["title"])
        self.clock = pg.time.Clock()
        pg.key.set_repeat(100, 100)
        self.build_path()
        self.load_data()

    def init_game_window(self):
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

    def build_path(self):
        self.game_folder = path.dirname(__file__)
        self.data_folder = path.join(self.game_folder, "data")
        self.img_folder = path.join(self.data_folder, "img")
        self.map_folder = path.join(self.data_folder, "maps")
        self.music_folder = path.join(self.data_folder, "music")
        self.sound_folder = path.join(self.data_folder, "sounds")
        self.fonts_folder = path.join(self.data_folder, "fonts")

    def load_img(self, source, scale, alpha):
        img = pg.image.load(path.join(self.img_folder, source))
        img = pg.transform.scale(img, scale)
        if alpha:
            img = img.convert_alpha()
        else:
            img = img.convert()
        return img

    def load_data(self):
        self.cursor_img = []
        self.weapon_vfx = []
        self.floor_img = []
        self.thrall_grave = []
        self.sleeper_grave = []
        self.pmove_img = []
        self.player_img = {}
        self.mob_img = {}
        self.grave_img = {}
        self.item_img = {}
        self.sounds = {}
        self.stances = ["magic", "coachgun"]
        tilesize = (self.settings["gen"]["tilesize"], self.settings["gen"]["tilesize"])

        # System Images
        self.undervoid_icon = self.load_img(
            self.settings["img"]["icon"], (64, 64), True
        )
        self.title_art = self.load_img(
            self.settings["img"]["title"],
            tuple(self.settings["gen"]["titledim"]),
            False,
        )
        self.rift_img = self.load_img(self.settings["img"]["rift"], tilesize, False)
        for img in self.settings["img"]["cursor"]:
            self.cursor_img.append(self.load_img(img, (64, 64), True))
        # Environment Images
        self.wall_img = self.load_img(
            self.settings["img"]["wall"]["voidwall"], tilesize, False
        )
        for img in self.settings["img"]["floor"]["dungeon"]:
            self.floor_img.append(self.load_img(img, tilesize, False))
        # Player Images
        for stance in self.stances:
            self.player_img[stance] = self.load_img(
                self.settings["img"]["player"]["voidwalker"]["stance"][stance],
                tuple((2 * x) for x in tilesize),
                True,
            )
        for img in self.settings["img"]["player"]["voidwalker"]["move"]:
            self.pmove_img.append(
                self.load_img(img, tuple((2 * x) for x in tilesize), True)
            )
        # Bullet Images
        self.vbullet_img = self.load_img(
            self.settings["img"]["bullets"]["void"]["bullet"], tilesize, True
        )
        for img in self.settings["img"]["bullets"]["void"]["fx"]:
            self.weapon_vfx.append(self.load_img(img, tilesize, True))
        # Mob Images
        self.mob_img["thrall"] = self.load_img(
            self.settings["img"]["mob"]["thrall"]["main"], tilesize, True
        )
        self.mob_img["sleeper"] = self.load_img(
            self.settings["img"]["mob"]["sleeper"]["main"], tilesize, True
        )
        self.grave_img["thrall"] = []
        self.grave_img["sleeper"] = []
        for img in self.settings["img"]["mob"]["thrall"]["grave"]:
            self.grave_img["thrall"].append(self.load_img(img, tilesize, True))
        for img in self.settings["img"]["mob"]["sleeper"]["grave"]:
            self.grave_img["sleeper"].append(self.load_img(img, tilesize, True))
        # Item Images
        for item in self.settings["img"]["items"]:
            self.item_img[item] = self.load_img(
                self.settings["img"]["items"][item],
                # https://stackoverflow.com/questions/1781970/multiplying-a-tuple-by-a-scalar
                tuple(int(0.75 * x) for x in tilesize),
                True,
            )

        for sound in self.settings["sounds"]:
            self.sounds[sound] = pg.mixer.Sound(
                path.join(self.sound_folder, self.settings["sounds"][sound])
            )

        pg.mouse.set_visible(False)
        pg.display.set_icon(self.undervoid_icon)

    def level(self, level):
        for sprite in self.all_sprites:
            if sprite != self.player and sprite != self.pmove:
                sprite.kill()
        for wall in self.walls:
            wall.kill()
        if level == "gen":
            self.map = Forge(self, self.settings["lvl"]["pieces"])
            self.map.load_all()
            self.map.new_surface(
                self.settings["lvl"]["tiles_wide"], self.settings["lvl"]["tiles_high"]
            )
        else:
            self.map = Forge(self, 1)
            self.map.load(level)
            self.map.new_surface(128, 128)
            if level == "temple.txt" and not self.init_player:
                self.player.hp = self.player.max_hp
        self.map.build_lvl()
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.cursor = Cursor(self)
        self.camera = Camera(self, self.map.width, self.map.height, self.cursor)
        self.mob_count = 0
        self.mob_max = self.settings["gen"]["mob_max"]

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.stops_bullets = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.graves = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()
        self.cursor_sprite = pg.sprite.Group()
        self.spawners = pg.sprite.Group()

        self.init_player = True
        # self.level("gen")
        self.level("temple.txt")
        # https://stackoverflow.com/questions/51973441/how-to-fade-from-one-colour-to-another-in-pygame
        self.base_color = choice(self.settings["void_colors"])
        self.next_color = choice(self.settings["void_colors"])
        self.change_every_x_seconds = 2
        self.number_of_steps = self.change_every_x_seconds * self.settings["gen"]["fps"]
        self.step = 1

        if self.settings["gen"]["music"] == "on":
            pg.mixer.music.load(
                path.join(self.music_folder, self.settings["music"]["leavinghome"])
            )
            pg.mixer.music.play(-1, 0.0)

    def run(self):
        self.playing = True
        while self.playing:
            # tick_busy_loop() uses more cpu but is more accurate
            self.dt = self.clock.tick_busy_loop(self.settings["gen"]["fps"]) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.spawners.update()
        self.camera.update(self.player)
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False, collide_hit_rect)
        for hit in hits:
            if hit.kind == "hp" and self.player.hp < self.settings["player"]["hp"]:
                hit.kill()
                if self.settings["gen"]["sound"] == "on":
                    self.sounds["treasure02"].play()
                self.player.add_hp(
                    self.settings["items"]["potions"]["red"]["hp"] * self.player.max_hp
                )
            if hit.kind == "gp":
                hit.kill()
                if self.settings["gen"]["sound"] == "on":
                    self.sounds["treasure03"].play()
                self.player.coins += 1
        # mobs hitting player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            now = pg.time.get_ticks()
            if now - hit.last_hit > self.settings["mob"]["thrall"]["dmg_rate"]:
                hit.last_hit = now
                self.player.hp -= self.settings["mob"]["thrall"]["dmg"]
                hit.vel = vec(0, 0)
                self.player.pos += vec(
                    self.settings["mob"]["thrall"]["knockback"], 0
                ).rotate(-hits[0].rot)
                if self.settings["gen"]["sound"] == "on":
                    self.sounds[(choice(self.settings["hit_sounds"]))].play()
            elif random() < 0.5:  # enemies get bounced back on ~50% of failed hits
                hit.pos += vec(self.settings["mob"]["thrall"]["knockback"], 0).rotate(
                    hits[0].rot
                )
            if self.player.hp <= 0:
                self.playing = False
        # bullets hitting mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.hp -= (
                self.settings["weapon"]["vbullet"]["dmg"]
                * self.settings["player"]["dmg_mult"]
            )
            # hit.vel = vec(0, 0)
        # https://stackoverflow.com/questions/51973441/how-to-fade-from-one-colour-to-another-in-pygame
        self.step += 1
        if self.step < self.number_of_steps:
            self.current_color = [
                x + (((y - x) / self.number_of_steps) * self.step)
                for x, y in zip(
                    pg.color.Color(self.base_color), pg.color.Color(self.next_color)
                )
            ]
        else:
            self.step = 1
            self.base_color = self.next_color
            self.next_color = choice(self.settings["void_colors"])
        self.bg_color = self.current_color

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(self.bg_color)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
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
            self.screen.blit(sprite.image, self.camera.apply(sprite))
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
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if self.inmenu:
                    if event.key == pg.K_RETURN:
                        self.selected = self.selected.split(" ")[0].strip(": ")
                        if self.selected == "new":
                            self.inmenu = False
                        elif self.selected == "settings":
                            self.menu_loop(self.menu_settings)
                        elif self.selected == "credits":
                            self.menu_loop(self.menu_credits)
                        elif self.selected == "exit":
                            self.quit()
                        elif self.selected == "back":
                            self.menu_loop(self.menu_main)
                        elif (
                            self.selected == "fullscreen"
                            or self.selected == "music"
                            or self.selected == "sound"
                        ):
                            if self.settings["gen"][self.selected] == "on":
                                self.settings["gen"][self.selected] = "off"
                                if self.selected == "music":
                                    pg.mixer.music.pause()
                            else:
                                self.settings["gen"][self.selected] = "on"
                                if self.selected == "music":
                                    pg.mixer.music.play(-1, 0.0)
                            self.update_settings()
                            self.menu_loop(self.menu_settings)
                    if event.key == pg.K_UP:
                        self.menu_index -= 1
                    elif event.key == pg.K_DOWN:
                        self.menu_index += 1

    def update_settings(self):
        with open("settings.yaml", "w") as f:
            yaml.dump(self.settings, f)
            f.close()
        self.menu_settings = [
            "fullscreen: {}".format(self.settings["gen"]["fullscreen"]),
            "music: {}".format(self.settings["gen"]["music"]),
            "sound: {}".format(self.settings["gen"]["sound"]),
            "back",
        ]

    # Text Renderer https://www.sourcecodester.com/tutorials/python/11784/python-pygame-simple-main-menu-selection.html
    def text_format(self, message, textFont, textSize, textColor):
        newFont = pg.font.SysFont(textFont, textSize)
        newText = newFont.render(message, 0, textColor)

        return newText

    def show_start_screen(self):
        self.font = "franklingothic"
        pg.mixer.music.load(
            path.join(self.music_folder, self.settings["music"]["voidwalk"])
        )
        if self.settings["gen"]["music"] == "on":
            pg.mixer.music.play(-1, 0.0)
        self.menu_main = ["new", "settings", "credits", "exit"]
        self.update_settings()
        self.menu_credits = ["back"]
        self.menu_index = 0
        self.menu_loop(self.menu_main)

    def show_go_screen(self):
        pass

    def menu_loop(self, menu_items):
        self.inmenu = True
        while self.inmenu:
            self.events()
            self.screen.fill(self.settings["colors"]["black"])
            self.screen.blit(
                self.title_art,
                (
                    (
                        self.settings["gen"]["width"]
                        - self.settings["gen"]["titledim"][0]
                    )
                    / 2,
                    50,
                ),
            )
            if self.menu_index > len(menu_items) - 1:
                self.menu_index = 0
            elif self.menu_index < 0:
                self.menu_index = len(menu_items) - 1
            self.selected = menu_items[self.menu_index]
            if menu_items is self.menu_credits:
                item_y = self.settings["gen"]["height"] - 100
                self.show_credits()
            else:
                item_y = 300
            fontsize = 80
            for item in menu_items:
                if item == self.selected:
                    color = self.settings["colors"]["white"]
                else:
                    color = self.settings["colors"]["mediumvioletred"]
                item_text = self.text_format(item.upper(), self.font, fontsize, color)
                self.screen.blit(
                    item_text,
                    (
                        self.settings["gen"]["width"] / 2
                        - (item_text.get_rect()[2] / 2),
                        item_y,
                    ),
                )
                item_y += fontsize
            pg.display.update()
            self.clock.tick_busy_loop(self.settings["gen"]["fps"])

    def show_credits(self):
        credits = [
            "Copyright (c) 2019 Matthew Geary",
            "",
            "Music:",
            '"Leaving Home" - Kevin MacLeod (incompetech.com)',
            '"voidwalk" - Matthew Geary',
            "The music for Undervoid is licensed under Creative Commons: By Attribution 4.0 License",
            "Found in `\data\music\MUSIC_LICENSE` or at http://creativecommons.org/licenses/by/4.0/",
            "",
            "In-game artwork by Matthew Geary.",
            "Title Art generated at https://fontmeme.com/pixel-fonts/",
            "",
            "LICENSE",
            'This program is licensed under the "MIT License".  Please',
            "see the file `LICENSE` in the source distribution of this",
            "software for license terms.",
        ]
        fontsize = 30
        line_y = 200
        for line in credits:
            credits_text = self.text_format(
                line, self.font, fontsize, self.settings["colors"]["white"]
            )
            self.screen.blit(
                credits_text,
                (
                    self.settings["gen"]["width"] / 2
                    - (credits_text.get_rect()[2] / 2),
                    line_y,
                ),
            )
            line_y += fontsize


if __name__ == "__main__":
    g = Game()
    g.show_start_screen()
    while True:
        g.new()
        g.run()
        g.show_go_screen()

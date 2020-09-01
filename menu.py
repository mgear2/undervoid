# Copyright (c) 2019 Matthew Geary
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml

yaml = ruamel.yaml.YAML()

class Menu:
    def __init__(self, client):
        self.client = client
        self.menu_index = 0
        self.menu_main = ["new", "multiplayer", "settings", "credits", "exit"]
        self.menu_multiplayer = ["back"]
        self.menu_credits = ["back"]
        self.menu_characters = client.data.characters + ["back"]

    def menu_loop(self, menu_items):
        """
        Menu loop: renders the menu options to screen and tracks which option the player has highlighted. 
        """
        self.inmenu = True
        while self.inmenu:
            if self.client.events() == "break":
                break
            self.client.screen.fill(self.client.settings["colors"]["black"])
            self.client.screen.blit(
                self.client.data.title_art,
                (
                    (
                        self.client.settings["gen"]["width"]
                        - self.client.settings["gen"]["titledim"][0]
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
                item_y = self.client.settings["gen"]["height"] - 100
                self.show_credits()
            else:
                item_y = 300
            fontsize = 80
            for item in menu_items:
                if item == self.selected:
                    color = self.client.settings["colors"]["white"]
                else:
                    color = self.client.settings["colors"]["mediumvioletred"]
                item_text = self.client.text_format(item.upper(), self.client.font, fontsize, color)
                self.client.screen.blit(
                    item_text,
                    (
                        self.client.settings["gen"]["width"] / 2
                        - (item_text.get_rect()[2] / 2),
                        item_y,
                    ),
                )
                item_y += fontsize
                if self.selected in self.menu_characters and self.selected != "back":
                    self.client.screen.blit(
                        pg.transform.scale(
                            self.client.data.player_img[self.selected]["move"][0], (320, 320)
                        ),
                        (
                            self.client.settings["gen"]["width"] / 2 - 170,
                            self.client.settings["gen"]["height"] / 2 + 25,
                        ),
                    )
                    self.client.screen.blit(
                        pg.transform.scale(
                            self.client.data.player_img[self.selected]["magic"], (320, 320)
                        ),
                        (
                            self.client.settings["gen"]["width"] / 2 - 160,
                            self.client.settings["gen"]["height"] / 2 + 25,
                        ),
                    )
            pg.display.update()
            self.client.clock.tick_busy_loop(self.client.settings["gen"]["fps"])

    def update_settings(self):
        """
        Updates the settings.yaml file based on player changes 
        in the settings menu. 
        """
        with open("settings.yaml", "w") as f:
            yaml.dump(self.client.settings, f)
            f.close()
        self.menu_settings = [
            "fullscreen: {}".format(self.client.settings["gen"]["fullscreen"]),
            "music: {}".format(self.client.settings["gen"]["music"]),
            "sound: {}".format(self.client.settings["gen"]["sound"]),
            "displayfps: {}".format(self.client.settings["gen"]["displayfps"]),
            "back",
        ]

    def show_credits(self):
        """
        Displayed upon selection of the credits menu. 
        """
        credits = [
            "Copyright (c) 2019 Matthew Geary",
            "",
            "Big thanks to Chris Bradfield's excellent pygame tutorial, which helped me",
            "enormously in getting started.",
            "Youtube: https://www.youtube.com/playlist?list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i",
            "Github: https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2023",
            "",
            "Music:",
            '"Leaving Home" - Kevin MacLeod (incompetech.com)',
            '"voidwalk" - Matthew Geary',
            "The music for Undervoid is licensed under Creative Commons: By Attribution 4.0 License",
            "Found in `\data\music\MUSIC_LICENSE` or at http://creativecommons.org/licenses/by/4.0/",
            "",
            "In-game artwork and sounds by Matthew Geary.",
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
            credits_text = self.client.text_format(
                line, self.client.font, fontsize, self.client.settings["colors"]["white"]
            )
            self.client.screen.blit(
                credits_text,
                (
                    self.client.settings["gen"]["width"] / 2
                    - (credits_text.get_rect()[2] / 2),
                    line_y,
                ),
            )
            line_y += fontsize
    
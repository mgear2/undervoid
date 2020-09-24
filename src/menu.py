# Copyright (c) 2020
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

import pygame as pg
import ruamel.yaml
import sys

yaml = ruamel.yaml.YAML()

# Text Renderer https://www.sourcecodester.com/tutorials/python/11784/python-pygame-simple-main-menu-selection.html
def text_format(
    message: str, textFont: str, textSize: int, textColor=[0, 0, 0]
) -> pg.font.Font:
    """
    Returns a pygame text ready to be drawn to screen.
    """
    newFont = pg.font.SysFont(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText


class Menu:
    def __init__(self, clock, screen, settings, data, font, character):
        self.clock, self.screen, self.settings, self.data, self.font, self.character = (
            clock,
            screen,
            settings,
            data,
            font,
            character,
        )
        self.menu_index = 0
        self.menu_main = ["new", "settings", "credits", "exit"]
        self.menu_credits = ["back"]
        self.menu_characters = self.data.characters + ["back"]
        self.update_settings()

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
                return self.menu_event(event)

    def quit(self):
        """
        Quits pygame and exits the program
        """
        pg.quit()
        sys.exit()

    def run(self, menu_items: list):
        """
        Menu loop: renders the menu options to screen and tracks which option the player has highlighted.
        """
        self.inmenu = True
        while self.inmenu:
            if self.events() in self.data.characters:
                return self.character
            self.screen.fill(self.settings["colors"]["black"])
            self.screen.blit(
                self.data.title_art,
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
                item_text = text_format(item.upper(), self.font, fontsize, color)
                self.screen.blit(
                    item_text,
                    (
                        self.settings["gen"]["width"] / 2
                        - (item_text.get_rect()[2] / 2),
                        item_y,
                    ),
                )
                item_y += fontsize
                if self.selected in self.menu_characters and self.selected != "back":
                    self.screen.blit(
                        pg.transform.scale(
                            self.data.player_img[self.selected]["move"][0],
                            (320, 320),
                        ),
                        (
                            self.settings["gen"]["width"] / 2 - 170,
                            self.settings["gen"]["height"] / 2 + 25,
                        ),
                    )
                    self.screen.blit(
                        pg.transform.scale(
                            self.data.player_img[self.selected]["magic"],
                            (320, 320),
                        ),
                        (
                            self.settings["gen"]["width"] / 2 - 160,
                            self.settings["gen"]["height"] / 2 + 25,
                        ),
                    )
            pg.display.update()
            self.clock.tick_busy_loop(self.settings["gen"]["fps"])

    def menu_event(self, event: pg.event):
        if event.key == pg.K_RETURN:
            self.selected = self.selected.split(" ")[0].strip(": ")
            if self.selected == "new":
                self.run(self.menu_characters)
            if self.selected in self.data.characters:
                self.character = self.selected
                self.inmenu = False
                return self.character
            elif self.selected == "settings":
                self.run(self.menu_settings)
            elif self.selected == "credits":
                self.run(self.menu_credits)
            elif self.selected == "exit":
                self.quit()
            elif self.selected == "back":
                self.run(self.menu_main)
            elif (
                self.selected == "fullscreen"
                or self.selected == "music"
                or self.selected == "sound"
                or self.selected == "displayfps"
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
                self.run(self.menu_settings)
        if event.key == pg.K_UP:
            self.menu_index -= 1
        elif event.key == pg.K_DOWN:
            self.menu_index += 1

    def update_settings(self):
        """
        Updates the settings.yaml file based on player changes
        in the settings menu.
        """
        with open("settings.yaml", "w") as f:
            yaml.dump(self.settings, f)
            f.close()
        self.menu_settings = [
            "fullscreen: {}".format(self.settings["gen"]["fullscreen"]),
            "music: {}".format(self.settings["gen"]["music"]),
            "sound: {}".format(self.settings["gen"]["sound"]),
            "displayfps: {}".format(self.settings["gen"]["displayfps"]),
            "back",
        ]

    def show_credits(self):
        """
        Displayed upon selection of the credits menu.
        """
        credits = [
            "Copyright (c) 2020",
            "Home: https://github.com/mgear2/undervoid",
            "",
            "Shoutout to Chris Bradfield's excellent pygame tutorial:",
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
            credits_text = text_format(
                line,
                self.font,
                fontsize,
                self.settings["colors"]["white"],
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

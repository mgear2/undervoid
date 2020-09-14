import pygame as pg
from random import choice


class Wall(pg.sprite.Sprite):
    """
    Walls come in three flavors:
    stops_bullets=True: visible walls
    stops_bullets=False: invisible walls
    stops_bullets="Rift": Rift
    """

    def __init__(
        self,
        settings,
        all_sprites,
        walls_group,
        stops_bullets_group,
        pos,
        stops_bullets,
    ):
        self.settings = settings
        self._layer = self.settings["layer"]["wall"]
        if stops_bullets == "Rift":
            self.groups = all_sprites, walls_group, stops_bullets_group
        elif stops_bullets == True:
            self.groups = walls_group, stops_bullets_group
        else:
            self.groups = walls_group
        self.stops_bullets = stops_bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.rect = pg.Rect(
            0,
            0,
            self.settings["gen"]["tilesize"],
            self.settings["gen"]["tilesize"],
        )
        self.rect.topleft = self.pos


class Rift(Wall):
    """
    Rifts allow players to move between levels.
    Rifts track distance to player to determine whether
    the player is within distance to use.
    """

    def __init__(
        self,
        settings,
        all_sprites,
        walls_group,
        stops_bullets_group,
        game_client_data_rift_img,
        pos,
    ):
        Wall.__init__(
            self, settings, all_sprites, walls_group, stops_bullets_group, pos, "Rift"
        )
        # self.game.rift_usable = False
        self.image = game_client_data_rift_img

    def check_usable(self, player_pos):
        self.target_dist = player_pos - self.pos
        if (
            self.target_dist.length_squared()
            < self.settings["lvl"]["rift_usable_distance"] ** 2
        ):
            return True
        return False

    def update(self, player_pos, game_level, game_client_data_biomes):
        if self.check_usable(player_pos):
            keys = pg.key.get_pressed()
            if keys[pg.K_e]:
                # current method of switching levels does not retain player data
                game_level("gen", choice(game_client_data_biomes))
            if keys[pg.K_r]:
                game_level("temple.txt", "void")

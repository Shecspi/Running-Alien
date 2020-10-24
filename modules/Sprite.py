#  Running Alien v. 0.3
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

import os
from random import randint


class Sprite:
    def __init__(self):
        self.__dir_sprites = 'resources/sprites/'
        self.__dir_coins = 'resources/sprites/coins/'
        self.__dir_clouds = 'resources/sprites/clouds/'
        self.__dir_enemies = 'resources/sprites/enemies/'
        self.__dir_special_enemies = 'resources/sprites/special_enemies/'
        self.__dir_player_stand = 'resources/sprites/player/stand/'
        self.__dir_player_run = 'resources/sprites/player/run/'
        self.__dir_player_jump = 'resources/sprites/player/jump/'
        self.__dir_player_hurt = 'resources/sprites/player/hurt/'
        self.__dir_platform = 'resources/sprites/grass/'
        self.__dir_button = 'resources/buttons/'

        self.__list_of_run_players: list = []
        self.__counter_run_player = 0

        self.__button_green = 'button_green.png'
        self.__button_green_shadow = 'button_green_shadow.png'
        self.__button_red = 'button_red.png'
        self.__button_red_shadow = 'button_red_shadow.png'
        self.__button_yellow = 'button_yellow.png'
        self.__button_yellow_shadow = 'button_yellow_shadow.png'

        self.__font = 'resources/fonts/Chilanka-Regular.ttf'

        self.__heart = 'heart.png'
        self.__platform_grass = 'grass_base.png'
        self.__coin_level_1 = 'coin.png'
        self.__coin_level_2 = 'ruby.png'
        self.__laser_gun = 'laser_gun.png'  # The name of file with laser gun
        self.__laser_line = 'laser_line.png'  # The name of file with laser line

        self.__generate_list_of_player_run()

    def __generate_list_of_player_run(self) -> None:
        """ Generate the list of files with run player.

        To make correct animation the files of running player should have the following names:
        ...1.png for first frame, ...2.png for second frame etc.

        """
        self.__list_of_run_players = sorted(os.listdir(self.__dir_player_run))

    def get_font(self) -> str:
        return self.__font

    def get_button(self, style) -> str:
        buttons_source = {
            'green': self.__dir_button + self.__button_green,
            'green_shadow': self.__dir_button + self.__button_green_shadow,
            'red': self.__dir_button + self.__button_red,
            'red_shadow': self.__dir_button + self.__button_red_shadow,
            'yellow': self.__dir_button + self.__button_yellow,
            'yellow_shadow': self.__dir_button + self.__button_yellow_shadow,
        }
        return buttons_source[style]

    def get_platform_grass(self) -> str:
        return self.__dir_platform + self.__platform_grass

    def get_random_player_jump(self) -> str:
        lst = os.listdir(self.__dir_player_jump)
        source = self.__dir_player_jump + lst[randint(0, len(lst) - 1)]
        return source

    def get_random_player_hurt(self) -> str:
        lst = os.listdir(self.__dir_player_hurt)
        source = self.__dir_player_hurt + lst[randint(0, len(lst) - 1)]
        return source

    def get_next_run_player_sprite(self) -> str:
        source = self.__dir_player_run + self.__list_of_run_players[self.__counter_run_player - 1]

        if self.__counter_run_player == len(self.__list_of_run_players) - 1:
            self.__counter_run_player = 0
        else:
            self.__counter_run_player += 1

        return source

    def get_coin_level_1(self) -> str:
        return self.__dir_coins + self.__coin_level_1

    def get_coin_level_2(self) -> str:
        return self.__dir_coins + self.__coin_level_2

    def get_laser_line(self) -> str:
        """ Return the full name of file with laser line.

        """
        return self.__dir_special_enemies + self.__laser_line

    def get_laser_gun(self) -> str:
        """ Return the full name of file with laser gun.

        """
        return self.__dir_special_enemies + self.__laser_gun

    def get_random_player_stand(self) -> str:
        """ Return the full name of file with random stand player.

        """
        lst = os.listdir(self.__dir_player_stand)
        source = self.__dir_player_stand + lst[randint(0, len(lst) - 1)]
        return source

    def get_random_cloud(self) -> str:
        """ Return the full name of file with random cloud.

        """
        lst = os.listdir(self.__dir_clouds)
        source = self.__dir_clouds + lst[randint(0, len(lst) - 1)]
        return source

    def get_random_enemy(self) -> str:
        """ Return the full name of file with random enemy.

        """
        lst = os.listdir(self.__dir_enemies)
        source = self.__dir_enemies + lst[randint(0, len(lst) - 1)]
        return source

    def get_heart(self) -> str:
        """ Return the full name of file with heart.

        """
        return self.__dir_sprites + self.__heart

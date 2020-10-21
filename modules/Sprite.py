#  Running Alien v. 0.1
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0
import os
from random import randint


class Sprite:
    def __init__(self):
        self.__dir_coins = 'resources/sprites/coins/'
        self.__dir_clouds = 'resources/sprites/clouds/'
        self.__dir_enemies = 'resources/sprites/enemies/'
        self.__dir_special_enemies = 'resources/sprites/special_enemies/'

        self.__coin_level_1 = 'coin.png'
        self.__coin_level_2 = 'ruby.png'
        self.__laser_gun = 'laser_gun.png'  # The name of file with laser gun
        self.__laser_line = 'laser_line.png'  # The name of file with laser line

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

    def get_random_cloud(self) -> str:
        """ Return the full name of file with random cloud.

        """
        lst = os.listdir(self.__dir_clouds)
        source = self.__dir_clouds + lst[randint(0, len(lst) - 1)]
        return source

    def get_random_enemy(self):
        """ Return the full name of file with random enemy.

        """
        lst = os.listdir(self.__dir_enemies)
        source = self.__dir_enemies + lst[randint(0, len(lst) - 1)]
        return source

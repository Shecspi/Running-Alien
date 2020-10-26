#  Running Alien v.0.4
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

import pygame

from modules.Setting import Setting
from modules.Sprite import Sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, y, sprite):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(sprite.get_random_player_stand()).convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(bottomleft=(150, y))

        # Spawn jump image or not
        self.__is_spawned: bool = False

        # 'True' if players moves to down else 'False'
        self.__is_moving_down: bool = False

        # An image of player
        self.__image_source: str = self.image

    def update(self,
               setting: Setting,
               sprite: Sprite,
               all_groups: dict,
               kill_instance: dict) -> str:
        """ Realize moving of player on Y-coordinate and check collide with other items.

        :param setting: An instance of 'Setting' class.
        :param sprite: An instance of 'Sprite' class.
        :param all_groups: A dict with groups of items.
        :param kill_instance: 'True' if it needs to kill item after collide or 'False' if no need.
        :return:
        """
        # Jumping
        if setting.get_is_jump():
            # On air
            if setting.get_counter_jump() >= - setting.get_counter_initial_jump():
                # Set an image for jumping player (if not set)
                if not self.__is_spawned:
                    self.__image_source = sprite.get_random_player_jump()
                    self.__is_spawned = True

                # If setting.get_counter_jump() > 0 it is moving to up
                if setting.get_counter_jump() > 0:
                    self.__is_moving_down = False
                    self.rect.y -= (setting.get_counter_jump() ** 2) // 2
                # If setting.get_counter_jump() > 0 it is moving to down
                elif setting.get_counter_jump() < 0:
                    self.__is_moving_down = True
                    self.rect.y += (setting.get_counter_jump() ** 2) // 2

                setting.set_counter_jump(setting.get_counter_jump() - 1)
            # On ground
            else:
                self.__is_spawned = False
                self.__is_moving_down = False
                self.__image_source = sprite.get_next_run_player_sprite()

                setting.set_is_jump(False)
                setting.reset_counter_jump()
        # Running
        else:
            self.__image_source = sprite.get_next_run_player_sprite()

        self.image = pygame.image.load(self.__image_source)

        return self.collide(all_groups, kill_instance)

    def collide(self,
                all_groups: dict,
                kill_instance: dict) -> str:
        """ Check collide between player and some items from 'all_group'.

        Can return the following values:
            - enemies
            - coin_regular
            - coin_laser
            - laser_line

        :param all_groups: A dict with groups of items.
        :param kill_instance: 'True' if it needs to kill item after collide or 'False' if no need.
        :return: The name of item.
        """
        for group_name in all_groups:
            hit = pygame.sprite.spritecollide(self, all_groups[group_name], False)
            for i in hit:
                if kill_instance[group_name]:
                    i.kill()
                return group_name
                # Moving down
                # if self.__is_moving_down:
                #     if self.rect.bottom >= enemy.rect.top:
                #         return 'TOP'
                # else:
                #     if self.rect.right >= enemy.rect.left:
                #         return 'LEFT'

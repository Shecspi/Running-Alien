#  Running Alien v.0.3
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0
from random import randint

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, y, sprite):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(sprite.get_random_player_stand()).convert_alpha()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(bottomleft=(150, y))

        # Spawn jump image or not
        self.__is_spawned: bool = False

        # An image of player
        self.__image_source: str = self.image

    def update(self, setting, sprite):
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
                    self.rect.y -= (setting.get_counter_jump() ** 2) // 2
                # If setting.get_counter_jump() > 0 it is moving to down
                elif setting.get_counter_jump() < 0:
                    self.rect.y += (setting.get_counter_jump() ** 2) // 2

                setting.set_counter_jump(setting.get_counter_jump() - 1)
            # On ground
            else:
                self.__is_spawned = False
                self.__image_source = sprite.get_next_run_player_sprite()

                setting.set_is_jump(False)
                setting.reset_counter_jump()
        # Running
        else:
            self.__image_source = sprite.get_next_run_player_sprite()

        self.image = pygame.image.load(self.__image_source)

#  Running Alien v.0.4
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

import pygame

from modules.Setting import Setting


class Enemy(pygame.sprite.Sprite):
    def __init__(self,
                 initial_x: int,
                 ground_line_y: int,
                 sprite,
                 group,
                 is_laser: bool,
                 is_died: bool = False):
        """ Initializate a new enemy.

        :param initial_x: X-coordinate of initialization place. Will be change every frame.
        :param ground_line_y: Y-coordinate of initialization place. It doesn't change.
        :param sprite: An instance of class 'Sprite'.
        :param group: A group of enemies.
        :param is_laser: 'True' if it's a laser, 'False' for other enemies.
        """
        pygame.sprite.Sprite.__init__(self)

        self.__image_source = sprite.get_laser_gun() if is_laser else sprite.get_random_enemy()
        self.image = pygame.image.load(self.__image_source).convert_alpha()
        self.__image_center_y = ground_line_y if is_died else ground_line_y - self.image.get_size()[1] // 2

        self.rect = self.image.get_rect(center=(initial_x, self.__image_center_y))

        self.add(group)

    def get_height(self) -> int:
        """ Return the height of enemy.

        """
        return self.rect.height

    def update(self,
               setting: Setting) -> None:
        """ Update X-coordinate every frame or kill enemy.

        :param setting: An instance of class 'Setting'.
        :return: None
        """
        if self.rect.x > 0 - self.rect.width:
            self.rect.x -= setting.get_speed_of_world()
        else:
            self.kill()

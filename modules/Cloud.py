#  Running Alien v.0.4
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0
from random import randint

import pygame


class Cloud(pygame.sprite.Sprite):
    def __init__(self,
                 initial_x: int,
                 sprite,
                 group):
        """ Initializate a new coin.

        :param initial_x: X-coordinate of initialization place. Will be change every frame.
        :param sprite: An instance of class 'Sprite'.
        :param group: A group of clouds.
        """
        pygame.sprite.Sprite.__init__(self)

        self.__image_source = sprite.get_random_cloud()
        self.image = pygame.image.load(self.__image_source).convert_alpha()

        self.rect = self.image.get_rect(center=(initial_x, randint(100, 300)))

        self.add(group)

    def update(self, setting):
        if self.rect.x > 0 - self.rect.width:
            self.rect.x -= setting.get_speed_of_world() // 2
        else:
            self.kill()

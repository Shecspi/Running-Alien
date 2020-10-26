#  Running Alien v.0.3
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

import pygame


class LaserLineEnemy(pygame.sprite.Sprite):
    def __init__(self, initial_x, y, sprite, group):
        pygame.sprite.Sprite.__init__(self)

        self.__image_source = sprite.get_laser_line()
        self.image = pygame.image.load(self.__image_source).convert_alpha()

        self.rect = self.image.get_rect(center=(initial_x, y))

        self.add(group)

    def update(self, setting):
        if self.rect.x > 0 - self.rect.width:
            self.rect.x -= setting.get_speed_of_world() + 8
        else:
            self.kill()

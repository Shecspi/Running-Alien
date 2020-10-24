#  Running Alien v.0.3
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

import pygame


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y, image, group):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

        self.add(group)

    def update(self, image, group, grass_x, qty_of_grass, grass_y, setting):
        if self.rect.x > 0 - self.rect.width:
            self.rect.x -= setting.get_speed_of_world()
        else:
            self.kill()
            self.__init__(self.rect.x + grass_x // 2 + qty_of_grass * grass_x - setting.get_speed_of_world(),
                          grass_y,
                          image,
                          group)

"""
Copyright 2020 Egor Vavilov (shecspi@gmail.com)
Licensed under the Apache License, Version 2.0
"""

import pygame

from setting import WORKPLACE_LEFT_SIDE


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y, image, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.add(group)

    def update(self, image, group, grass_x, qty_of_grass, speed_of_world, grass_y):
        # Сдвигаем спрайты влево на 5 пикселей.
        # Если спрайт ушел полностью за экран - уничтожаем его.
        if self.rect.x > WORKPLACE_LEFT_SIDE - grass_x:
            self.rect.x -= speed_of_world
        else:
            self.kill()
            self.__init__(self.rect.x + grass_x // 2 + qty_of_grass * grass_x - speed_of_world,
                          grass_y,
                          image,
                          group)

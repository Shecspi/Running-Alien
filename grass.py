"""
Copyright 2020 Egor Vavilov (shecspi@gmail.com)
Licensed under the Apache License, Version 2.0
"""

import pygame

from setting import WORKPLACE_LEFT_SIDE


class Grass(pygame.sprite.Sprite):
    def __init__(self, x, y, surf, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, y))
        self.add(group)

    def update(self, image, group, grass_width, qty_of_grass, speed_of_world):
        # Сдвигаем спрайты влево на 5 пикселей.
        # Если спрайт ушел полностью за экран - уничтожаем его.
        if self.rect.x > WORKPLACE_LEFT_SIDE - grass_width:
            self.rect.x -= speed_of_world
        else:
            self.kill()
            self.__init__(self.rect.x + grass_width // 2 + qty_of_grass * grass_width - speed_of_world, self.rect.y + grass_width // 2, image, group)
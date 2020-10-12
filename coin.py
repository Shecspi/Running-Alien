"""
Copyright 2020 Egor Vavilov (shecspi@gmail.com)
Licensed under the Apache License, Version 2.0
"""

import pygame

import setting


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, image, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.add(group)

    def update(self):
        if self.rect.x > setting.WORKPLACE_LEFT_SIDE - self.rect.width:
            self.rect.x -= setting.speed_of_world
        else:
            self.kill()

#  Running Alien v.0.2
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

import pygame


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, image, group):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

        self.add(group)

    def update(self, speed_of_world):
        if self.rect.x > 0 - self.rect.width:
            self.rect.x -= speed_of_world // 2
        else:
            self.kill()

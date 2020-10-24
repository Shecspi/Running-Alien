#  Running Alien v.0.3
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, y, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(bottomleft=(150, y))

    def update(self, image, running=True, is_jump=False, jump_count=0):
        if running and is_jump:
            if jump_count > 0:
                self.rect.y -= (jump_count ** 2) // 2
            elif jump_count < 0:
                self.rect.y += (jump_count ** 2) // 2

        self.image = pygame.image.load(image)

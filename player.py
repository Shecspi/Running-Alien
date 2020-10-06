import pygame
from loguru import logger

import config


class Player(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/p3_walk01.png').convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (150, y)

    def update(self, image, running=True):
        if running:
            if config.is_jump:
                if config.jump_count > 0:
                    self.rect.y -= (config.jump_count ** 2) // 2
                elif config.jump_count < 0:
                    self.rect.y += (config.jump_count ** 2) // 2

        self.image = pygame.image.load(image)

import pygame as pygame

import setting
from setting import WORKPLACE_LEFT_SIDE


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, image, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.add(group)
        self.rect.center = (x, y)

    def update(self):
        if self.rect.x > WORKPLACE_LEFT_SIDE - self.image.get_size()[0]:
            self.rect.x -= setting.speed_of_world // 2
        else:
            self.kill()

import pygame


class Score(pygame.sprite.Sprite):
    def __init__(self, x, y, image, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.add(group)
        self.rect.bottomleft = (x, y)

    def update(self):
        self.kill()

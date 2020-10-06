import pygame


class Score:
    def __init__(self, screen: pygame.Surface, font: str, size: int):
        self.screen: pygame.Surface = screen
        self.font_src: str = font
        self.size: int = size
        self.text: str = ''

    def set_text(self, text, x, y, right_align = False):
        font = pygame.font.Font(self.font_src, self.size)
        self.text = font.render(text, 1, (0, 0, 0))
        if not right_align:
            rect = self.text.get_rect(bottomleft=(x, y))
        else:
            rect = self.text.get_rect(bottomright=(x, y))
        self.screen.blit(self.text, rect)

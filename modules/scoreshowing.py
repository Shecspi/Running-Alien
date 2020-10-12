import pygame


class ScoreShowing:
    def __init__(self, screen):
        self.x = 30
        self.y = 30
        self.font_size = 24
        self.font_color = (0, 0, 0)
        self.current_result_height = 0
        self.current_result_width = 0
        self.screen = screen

    def current_score(self, score):
        """
        Draws the current result in the left top corner of screen.
        :param score: The current result
        :return: None
        """
        font = pygame.font.Font('sprites/fonts/kenvector_future_thin.ttf', self.font_size)
        text = font.render(f'Score: {score}', 1, self.font_color)
        text_rect = text.get_rect(topleft=(self.x, self.y))

        self.current_result_width, self.current_result_height = text.get_size()
        self.screen.blit(text, text_rect)

    def best_score(self, score):
        """
        Draws the best result in the left top corner of screen.
        :param score: the best result
        :return: None
        """
        font = pygame.font.Font('sprites/fonts/kenvector_future_thin.ttf', self.font_size)
        text = font.render(f'The best result: {score}', 1, self.font_color)
        text_rect = text.get_rect(topleft=(self.x, self.y + self.current_result_height + 10))

        self.screen.blit(text, text_rect)

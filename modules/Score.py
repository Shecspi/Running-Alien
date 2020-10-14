#  Running Alien v. 0.1
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

""" Display the information about score - current and best.

This class has two public methods:
    'display_current_score' - to display current score on the screen;
    'display_best_score' - to display best score in the screen.

"""

import pygame


class Score:
    def __init__(self, screen):
        self.x = 30
        self.y = 30
        self.font_size = 24
        self.font_color = (0, 0, 0)
        self.font_src = 'sprites/fonts/kenvector_future_thin.ttf'
        self.current_result_height = 0
        self.current_result_width = 0
        self.screen = screen

    def __draw_text(self,
                    x: int,
                    y: int,
                    message: str,
                    size: int
                    ) -> pygame.Rect:
        """ Displays text on the screen.

        :param x: X-coordinate for center of text
        :param y: Y-coordinate for center of text
        :param message: Text,
        :param size: Size of font
        :return: pygame.Rect of this text
        """
        font = pygame.font.Font(self.font_src, size)
        text = font.render(message, 1, self.font_color)
        text_rect = text.get_rect(topleft=(x, y))

        self.screen.blit(text, text_rect)

        return text_rect

    def display_current_score(self, score):
        """  Draws the current result in the left top corner of screen.

        :param score: The current result
        :return: None
        """
        text = self.__draw_text(self.x, self.y, f'Score: {score}', self.font_size)
        self.current_result_width = text.height

    def display_best_score(self, score):
        """ Draws the best result in the left top corner of screen.

        :param score: The best result
        :return: None
        """
        self.__draw_text(self.x,
                         self.y + self.current_result_width,
                         f'The best result: {score}',
                         self.font_size)

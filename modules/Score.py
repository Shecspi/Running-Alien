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
        self.current_score = 0
        self.best_score = 0

        self.__x = 30
        self.__y = 30
        self.__font_size = 24
        self.__font_color = (0, 0, 0)
        self.__font_src = 'sprites/fonts/kenvector_future_thin.ttf'
        self.__current_result_height = 0
        self.__screen = screen

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
        font = pygame.font.Font(self.__font_src, size)
        text = font.render(message, 1, self.__font_color)
        text_rect = text.get_rect(topleft=(x, y))

        self.__screen.blit(text, text_rect)

        return text_rect

    def set_current_score(self, score: int) -> None:
        """ Set the current score value.

        :param score: The current score
        :return: None
        """
        self.current_score = score

    def set_best_score(self, score: int) -> None:
        """ Set the best score value.

        :param score: The best score
        :return: None
        """
        self.best_score = score

    def get_current_score(self) -> int:
        """ Returns the current score value.

        :return: int
        """
        return self.current_score

    def get_best_score(self) -> int:
        """ Returns the best score value.

        :return: int
        """
        return self.best_score

    def display_current_score(self,):
        """  Draws the current result in the left top corner of screen.

        :return: None
        """
        text = self.__draw_text(self.__x, self.__y, f'Score: {self.current_score}', self.__font_size)
        self.__current_result_height = text.height

    def display_best_score(self):
        """ Draws the best result in the left top corner of screen.

        :return: None
        """
        self.__draw_text(self.__x,
                         self.__y + self.__current_result_height,
                         f'The best result: {self.best_score}',
                         self.__font_size)

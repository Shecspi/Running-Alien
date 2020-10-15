#  Running Alien v.0.2
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

""" Draws some menu on the screen.

This class has three public method:
    'display_start_menu' to display start menu;
    'display_pause_menu' to display pause menu;
    'display_death_menu' to display death menu.
All these methods return a string depending on which button was clicked.

"""

import pygame
from loguru import logger


class ScreenMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.font_src = 'sprites/fonts/kenvector_future_thin.ttf'
        self.font_size_regular = 24
        self.font_size_copyright = 16
        self.font_size_title = 100
        self.font_color = (0, 0, 0)
        self.background = pygame.image.load("sprites/menu_background.jpg").convert_alpha()

    def __draw_button(self,
                      x: int,
                      y: int,
                      image_src: str,
                      message: str
                      ) -> pygame.Rect:
        """
        Draws a button on the screen.
        :param x: X-coordinate for center of button
        :param y: Y-coordinate for center of button
        :param image_src: Source of image for button
        :param message: Text to show on the button
        :return: The button size
        """
        image = pygame.image.load(image_src).convert_alpha()
        image_rect = image.get_rect(center=(x, y))

        self.screen.blit(image, image_rect)
        self.__draw_text(x, y, message, self.font_size_regular)

        return image_rect

    def __draw_text(self,
                    x: int,
                    y: int,
                    message: str,
                    size: int
                    ) -> pygame.Rect:
        """
        Displays text on the screen.
        :param x: X-coordinate for center of text
        :param y: Y-coordinate for center of text
        :param message: Text,
        :param size: Size of font
        :return: pygame.Rect of this text
        """
        font = pygame.font.Font(self.font_src, size)
        text = font.render(message, 1, self.font_color)
        text_rect = text.get_rect(center=(x, y))

        self.screen.blit(text, text_rect)

        return text_rect

    def __draw_copyright(self,
                         x: int,
                         y: int):
        """
        Displays the copyright for some menu.
        :param x:  Coordinate X for center of text
        :param y: Coordinate Y for center of text
        :return: None
        """
        copyright_rect = self.__draw_text(x,
                                          y,
                                          'Copyright 2020 Egor Vavilov (shecspi@gmail.com)',
                                          self.font_size_copyright)
        self.__draw_text(self.screen_width // 2,
                         copyright_rect.y + copyright_rect.height + 20,
                         'Licensed under the Apache License, Version 2.0',
                         self.font_size_copyright)

    @staticmethod
    def __handle_mouse_press(element_rect: pygame.Rect,
                             mouse_position: tuple
                             ) -> bool:
        """
        Check of click coordinates 'mouse_position' are on coordinates 'element_rect',
        If yes, return 'True', else 'False'.
        :param element_rect: Coordinates of interface element
        :param mouse_position: Coordinates of mouse click
        :return: bool
        """
        x0, y0, width, height = element_rect
        x1 = x0 + width
        y1 = y0 + height

        if x0 <= mouse_position[0] <= x1 and y0 <= mouse_position[1] <= y1:
            return True
        else:
            return False

    def display_start_menu(self, position_of_click) -> str:
        """
        Displays the start menu of the game (before the gaming).
        Displays title, two buttons 'Start' and 'Exit', the copyright information.
        :param position_of_click: Coordinates of mouse after click.
        :return: Keyword of pressed button - 'start' of 'exit'
        """
        self.screen.blit(self.background, (0, 0), None, pygame.BLEND_RGBA_SUB)

        # Title "Are you ready?"
        title_rect = self.__draw_text(self.screen_width // 2,
                                      150,
                                      'Are you ready?',
                                      self.font_size_title)
        # Button "Start"
        start_rect = self.__draw_button(self.screen_width // 2,
                                        title_rect.y + title_rect.height + 50,
                                        'sprites/green_button.png',
                                        'Start')
        # Button "Reset"
        reset_rect = self.__draw_button(self.screen_width // 2,
                                        start_rect.y + start_rect.height + 50,
                                        'sprites/red_button.png',
                                        'Reset')
        # Button "Exit"
        exit_rect = self.__draw_button(self.screen_width // 2,
                                       reset_rect.y + reset_rect.height + 50,
                                       'sprites/red_button.png',
                                       'Exit')
        # Copyright
        self.__draw_copyright(self.screen_width // 2, exit_rect.y + exit_rect.height + 50)

        if position_of_click:
            if self.__handle_mouse_press(start_rect, position_of_click):
                logger.info("The button 'Start' was pressed.")
                return 'start'
            elif self.__handle_mouse_press(reset_rect, position_of_click):
                logger.info("The button 'Reset' was pressed.")
                return 'reset'
            elif self.__handle_mouse_press(exit_rect, position_of_click):
                logger.info("The button 'Exit' was pressed.")
                return 'exit'

    def display_pause_menu(self, position_of_click):
        """
        Displays the pause menu of the game.
        Displays title, two buttons 'Start' and 'Exit', the copyright information.
        :param position_of_click: Coordinates of mouse after click.
        :return: Keyword of pressed button - 'resume' of 'exit'
        """
        # Отображает фоновое полупрозрачное изображение поверх сцены с игрой
        self.screen.blit(self.background, (0, 0), None, pygame.BLEND_RGBA_SUB)

        # Title "Pause"
        pause_rect = self.__draw_text(self.screen_width // 2,
                                      150,
                                      'Pause',
                                      self.font_size_title)
        # Button "Resume"
        resume_rect = self.__draw_button(self.screen_width // 2,
                                         pause_rect.y + pause_rect.height + 50,
                                         'sprites/green_button.png',
                                         'Resume')
        # Кнопка "Exit"
        exit_rect = self.__draw_button(self.screen_width // 2,
                                       resume_rect.y + resume_rect.height + 50,
                                       'sprites/red_button.png',
                                       'Exit')
        # Copyright
        self.__draw_copyright(self.screen_width // 2,
                              exit_rect.y + exit_rect.height + 50)

        if position_of_click:
            if self.__handle_mouse_press(resume_rect, position_of_click):
                logger.info("The button 'Resume' was pressed.")
                return 'resume'
            if self.__handle_mouse_press(exit_rect, position_of_click):
                logger.info("The button 'Exit' was pressed.")
                return 'exit'

    def display_death_menu(self, position_of_click):
        """
        Displays the menu of the game when player was died.
        Displays title, two buttons 'Restart' and 'Exit', the copyright information.
        :param position_of_click: Coordinates of mouse after click.
        :return: Keyword of pressed button - 'restart' of 'exit'
        """
        self.screen.blit(self.background, (0, 0), None, pygame.BLEND_RGBA_SUB)

        # Title "Game over"
        title_rect = self.__draw_text(self.screen_width // 2,
                                      150,
                                      'Game over',
                                      self.font_size_title)
        # Button "Restart"
        restart_rect = self.__draw_button(self.screen_width // 2,
                                          title_rect.y + title_rect.height + 50,
                                          'sprites/green_button.png',
                                          'Restart')
        # Button "Exit"
        exit_rect = self.__draw_button(self.screen_width // 2,
                                       restart_rect.y + restart_rect.height + 50,
                                       'sprites/red_button.png',
                                       'Exit')
        # Copyright
        self.__draw_copyright(self.screen_width // 2,
                              exit_rect.y + exit_rect.height + 50)

        if position_of_click:
            if self.__handle_mouse_press(restart_rect, position_of_click):
                logger.info("The button 'Restart' was pressed.")
                return 'restart'
            if self.__handle_mouse_press(exit_rect, position_of_click):
                logger.info("The button 'Exit' was pressed.")
                return 'exit'

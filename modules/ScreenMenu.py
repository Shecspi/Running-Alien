#  Running Alien v.0.3
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
    def __init__(self, screen, sprite):
        self.__screen = screen
        self.__screen_width, self.screen_height = self.__screen.get_size()

        self.__font_color = (0, 0, 0)
        self.__font_src = sprite.get_font()
        self.__font_size_regular = 30
        self.__font_size_button = 24
        self.__font_size_copyright = 20
        self.__font_size_title = 70

        self.__red_button = sprite.get_button('red')
        self.__red_shadow_button = sprite.get_button('red_shadow')
        self.__green_button = sprite.get_button('green')
        self.__green_shadow_button = sprite.get_button('green_shadow')
        self.__yellow_button = sprite.get_button('yellow')
        self.__yellow_shadow_button = sprite.get_button('yellow_shadow')

        self.__background = pygame.image.load("resources/background/menu.jpg").convert_alpha()

    def __draw_button(self,
                      x: int,
                      y: int,
                      image_regular_src: str,
                      image_shadow_src: str,
                      message: str,
                      mouse_position: tuple
                      ) -> pygame.Rect:
        """ Draws a button on the screen.

        :param x: X-coordinate for center of button
        :param y: Y-coordinate for center of button
        :param image_regular_src: Source of regular image for button (in focus condition)
        :param image_shadow_src: Source of image for button with shadow (usual condition)
        :param message: Text to show on the button
        :param mouse_position The current mouse position
        :return: The button size
        """
        image_regular = pygame.image.load(image_regular_src).convert_alpha()
        image_regular_rect = image_regular.get_rect(center=(x, y))
        image_shadow = pygame.image.load(image_shadow_src).convert_alpha()
        image_shadow_rect = image_shadow.get_rect(center=(x, y))

        if self.__checking_mouse_position(image_regular_rect, mouse_position):
            self.__screen.blit(image_regular, image_regular_rect)
        else:
            self.__screen.blit(image_shadow, image_shadow_rect)

        self.__draw_text(x, y, message, self.__font_size_button)

        return image_shadow_rect

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
        :return: The text size
        """
        font = pygame.font.Font(self.__font_src, size)
        text = font.render(message, 1, self.__font_color)
        text_rect = text.get_rect(center=(x, y))

        self.__screen.blit(text, text_rect)

        return text_rect

    def __draw_copyright(self,
                         x: int,
                         y: int) -> None:
        """ Displays the copyright for some menu.

        :param x:  Coordinate X for center of text
        :param y: Coordinate Y for center of text
        :return: None
        """
        copyright_rect = self.__draw_text(x,
                                          y,
                                          'Copyright © 2020 Egor Vavilov (shecspi@gmail.com)',
                                          self.__font_size_copyright)
        self.__draw_text(self.__screen_width // 2,
                         copyright_rect.y + copyright_rect.height + 20,
                         'Licensed under the Apache License, Version 2.0',
                         self.__font_size_copyright)

    @staticmethod
    def __checking_mouse_position(element_rect: pygame.Rect,
                                  mouse_position: tuple
                                  ) -> bool:
        """ Check of mouse position 'mouse_position' are on coordinates 'element_rect',

        If yes, return 'True', else 'False'.
        :param element_rect: Coordinates of interface element
        :param mouse_position: Coordinates of mouse
        :return: bool
        """
        x0, y0, width, height = element_rect
        x1 = x0 + width
        y1 = y0 + height

        if x0 <= mouse_position[0] <= x1 and y0 <= mouse_position[1] <= y1:
            return True
        else:
            return False

    def display_start_menu(self,
                           mouse_position: tuple,
                           is_clicked: bool) -> str:
        """ Displays the start menu of the game (before the gaming).

        Displays title, two buttons 'Start' and 'Exit', the copyright information.
        :param mouse_position: The current mouse position
        :param is_clicked: 'True' if it was a click, else 'False'
        :return: Keyword of pressed button - 'start' of 'exit'
        """
        self.__screen.blit(self.__background, (0, 0), None, pygame.BLEND_RGBA_SUB)

        # Title
        title_rect = self.__draw_text(self.__screen_width // 2,
                                      150,
                                      'Running Alien ver. 0.2',
                                      self.__font_size_title)
        # Button "Start"
        start_rect = self.__draw_button(self.__screen_width // 2,
                                        title_rect.y + title_rect.height + 50,
                                        self.__green_button,
                                        self.__green_shadow_button,
                                        'Start',
                                        mouse_position)
        # Button "Reset"
        reset_rect = self.__draw_button(self.__screen_width // 2,
                                        start_rect.y + start_rect.height + 50,
                                        self.__red_button,
                                        self.__red_shadow_button,
                                        'Reset',
                                        mouse_position)
        # # Button "Exit"
        exit_rect = self.__draw_button(self.__screen_width // 2,
                                       reset_rect.y + reset_rect.height + 50,
                                       self.__red_button,
                                       self.__red_shadow_button,
                                       'Exit',
                                       mouse_position)
        # # Copyright
        self.__draw_copyright(self.__screen_width // 2, exit_rect.y + exit_rect.height + 50)

        if is_clicked:
            if self.__checking_mouse_position(start_rect, mouse_position):
                logger.info("The button 'Start' was pressed.")
                return 'start'
            elif self.__checking_mouse_position(reset_rect, mouse_position):
                logger.info("The button 'Reset' was pressed.")
                return 'reset'
            elif self.__checking_mouse_position(exit_rect, mouse_position):
                logger.info("The button 'Exit' was pressed.")
                return 'exit'

    def display_pause_menu(self,
                           mouse_position,
                           is_clicked) -> str:
        """
        Displays the pause menu of the game.
        Displays title, two buttons 'Start' and 'Exit', the copyright information.
        :param mouse_position: The current mouse position
        :param is_clicked: 'True' if it was a click, else 'False'
        :return: Keyword of pressed button - 'resume' or 'exit'
        """
        # Отображает фоновое полупрозрачное изображение поверх сцены с игрой
        self.__screen.blit(self.__background, (0, 0), None, pygame.BLEND_RGBA_SUB)

        # Title "Pause"
        pause_rect = self.__draw_text(self.__screen_width // 2,
                                      150,
                                      'Pause',
                                      self.__font_size_title)
        # Button "Resume"
        resume_rect = self.__draw_button(self.__screen_width // 2,
                                         pause_rect.y + pause_rect.height + 50,
                                         self.__green_button,
                                         self.__green_shadow_button,
                                         'Resume',
                                         mouse_position)
        # Кнопка "Exit"
        exit_rect = self.__draw_button(self.__screen_width // 2,
                                       resume_rect.y + resume_rect.height + 50,
                                       self.__red_button,
                                       self.__red_shadow_button,
                                       'Exit',
                                       mouse_position)
        # Copyright
        self.__draw_copyright(self.__screen_width // 2,
                              exit_rect.y + exit_rect.height + 50)

        if is_clicked:
            if self.__checking_mouse_position(resume_rect, mouse_position):
                logger.info("The button 'Resume' was pressed.")
                return 'resume'
            if self.__checking_mouse_position(exit_rect, mouse_position):
                logger.info("The button 'Exit' was pressed.")
                return 'exit'

    def display_death_menu(self,
                           mouse_position: tuple,
                           is_clicked: bool) -> str:
        """
        Displays the menu of the game when player was died.
        Displays title, two buttons 'Restart' and 'Exit', the copyright information.
        :param mouse_position: The current mouse position
        :param is_clicked: 'True' if it was a click, else 'False'
        :return: Keyword of pressed button - 'restart' or 'exit'
        """
        self.__screen.blit(self.__background, (0, 0), None, pygame.BLEND_RGBA_SUB)

        # Title "Game over"
        title_rect = self.__draw_text(self.__screen_width // 2,
                                      150,
                                      'Game over',
                                      self.__font_size_title)
        # Button "Restart"
        restart_rect = self.__draw_button(self.__screen_width // 2,
                                          title_rect.y + title_rect.height + 50,
                                          self.__green_button,
                                          self.__green_shadow_button,
                                          'Restart',
                                          mouse_position)
        # Button "Exit"
        exit_rect = self.__draw_button(self.__screen_width // 2,
                                       restart_rect.y + restart_rect.height + 50,
                                       self.__red_button,
                                       self.__red_shadow_button,
                                       'Exit',
                                       mouse_position)
        # Copyright
        self.__draw_copyright(self.__screen_width // 2,
                              exit_rect.y + exit_rect.height + 50)

        if is_clicked:
            if self.__checking_mouse_position(restart_rect, mouse_position):
                logger.info("The button 'Restart' was pressed.")
                return 'restart'
            if self.__checking_mouse_position(exit_rect, mouse_position):
                logger.info("The button 'Exit' was pressed.")
                return 'exit'

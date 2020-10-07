"""
Copyright 2020 Egor Vavilov (shecspi@gmail.com)
Licensed under the Apache License, Version 2.0
"""

from random import randint

import pygame
from loguru import logger

import config
from coin import Coin
from setting import *
from grass import Grass
from player import Player
from enemies import Enemie

# TODO Избавиться от обращения к глобальным переменным, таких как 'screen'


def start_menu(pos: tuple):
    """
    Displays the start menu of the game (before the gaming).
    Displays title, two buttons 'Start' and 'Exit', the copyright information.
    :param pos: Coordinates of mouse after click. You can use this parameter for handling button presses.
    :return: Keyword of pressed button - 'start' of 'exit'
    """
    screen.blit(pause_background, (0, 0), None, pygame.BLEND_RGBA_SUB)

    # Title "Are you ready?"
    title_rect = menu_text(WORKPLACE_X // 2, 150, 'Are you ready?', 100)
    title_bottom_y = title_rect.y + title_rect.height

    # Button "Start"
    start_rect = menu_button('sprites/green_button.png', WORKPLACE_X // 2, title_bottom_y + 50, 'Start', screen)
    start_rect_y = start_rect.y + start_rect.height

    # Button "Exit"
    exit_rect = menu_button('sprites/red_button.png', WORKPLACE_X // 2, start_rect_y + 50, 'Exit', screen)
    exit_rect_y = exit_rect.y + exit_rect.height

    # Copyright
    display_copyright(WORKPLACE_X // 2, exit_rect_y + 50)

    if pos:
        if handle_mouse_press(start_rect, pos):
            logger.info("The button 'Start' was pressed.")
            return 'start'
        if handle_mouse_press(exit_rect, pos):
            logger.info("The button 'Exit' was pressed.")
            return 'exit'


def pause_menu(pos):
    """
    Displays the pause menu of the game.
    Displays title, two buttons 'Start' and 'Exit', the copyright information.
    :param pos: Coordinates of mouse after click. You can use this parameter for handling button presses.
    :return: Keyword of pressed button - 'resume' of 'exit'
    """
    # Отображает фоновое полупрозрачное изображение поверх сцены с игрой
    screen.blit(pause_background, (0, 0), None, pygame.BLEND_RGBA_SUB)

    # Title "Pause"
    pause_rect = menu_text(WORKPLACE_X // 2, 150, 'Pause', 100)
    pause_bottom_y = pause_rect.y + pause_rect.height

    cloud_font = pygame.font.Font('sprites/fonts/kenvector_future_thin.ttf', 24)

    # Кнопка "Resume"
    resume_rect = menu_button('sprites/green_button.png', WORKPLACE_X // 2, pause_bottom_y + 50, 'Resume', screen)
    resume_rect_y = resume_rect.y + resume_rect.height

    # Кнопка "Exit"
    exit_rect = menu_button('sprites/red_button.png', WORKPLACE_X // 2, resume_rect_y + 50, 'Exit', screen)
    exit_rect_y = exit_rect.y + exit_rect.height

    # Copyright
    display_copyright(WORKPLACE_X // 2, exit_rect_y + 50)

    if pos:
        if handle_mouse_press(resume_rect, pos):
            logger.info("The button 'Resume' was pressed.")
            return 'resume'
        if handle_mouse_press(exit_rect, pos):
            logger.info("The button 'Exit' was pressed.")
            return 'exit'


def died_menu(pos):
    """
    Displays the menu of the game when player was died.
    Displays title, two buttons 'Restart' and 'Exit', the copyright information.
    :param pos: Coordinates of mouse after click. You can use this parameter for handling button presses.
    :return: Keyword of pressed button - 'restart' of 'exit'
    """
    screen.blit(pause_background, (0, 0), None, pygame.BLEND_RGBA_SUB)

    # Title "Game over"
    game_over_rect = menu_text(WORKPLACE_X // 2, 150, 'Pause', 100)
    game_over_y = game_over_rect.y + game_over_rect.height

    # Button "Restart"
    restart_rect = menu_button('sprites/green_button.png', WORKPLACE_X // 2, game_over_y + 50, 'Restart', screen)
    restart_rect_y = restart_rect.y + restart_rect.height

    # Button "Exit"
    exit_rect = menu_button('sprites/red_button.png', WORKPLACE_X // 2, restart_rect_y + 50, 'Exit', screen)
    exit_rect_y = exit_rect.y + exit_rect.height

    # Copyright
    display_copyright(WORKPLACE_X // 2, exit_rect_y + 50)

    if pos:
        if handle_mouse_press(restart_rect, pos):
            logger.info("The button 'Restart' was pressed.")
            return 'restart'
        if handle_mouse_press(exit_rect, pos):
            logger.info("The button 'Exit' was pressed.")
            return 'exit'


def display_copyright(x, y):
    """
    Displays the copyright for some menu.
    :param x:  Coordinate X for center of text
    :param y: Coordinate Y for center of text
    :return: None
    """
    copyright_rect = menu_text(x, y, 'Copyright 2020 Egor Vavilov (shecspi@gmail.com)', 16)
    copyright_rect_y = copyright_rect.y + copyright_rect.height
    menu_text(WORKPLACE_X // 2, copyright_rect_y + 20, 'Licensed under the Apache License, Version 2.0', 16)


def menu_text(x, y, message, font_size, align='center'):
    """
    Displays text on the screen.
    :param x: Coordinate X for center of text
    :param y: Coordinate Y for center of text
    :param message: Text
    :param font_size: Size of font
    :param align: Alignment of text ('left', 'right' or 'center')
    :return: pygame.Rect of this text
    """
    font_src = pygame.font.Font('sprites/fonts/kenvector_future_thin.ttf', font_size)
    title = font_src.render(message, 1, (0, 0, 0))
    if align == 'left':
        title_rect = title.get_rect(bottomleft=(x, y))
    elif align == 'right':
        title_rect = title.get_rect(bottomright=(x, y))
    else:
        title_rect = title.get_rect(center=(x, y))
    screen.blit(title, title_rect)

    return title_rect


def menu_button(image_src, x, y, message, display):
    font = pygame.font.Font('sprites/fonts/kenvector_future_thin.ttf', 24)

    image = pygame.image.load(image_src).convert_alpha()
    image_rect = image.get_rect(center=(x, y))
    text = font.render(message, 1, (0, 0, 0))
    text_rect = text.get_rect(center=(x, y))

    display.blit(image, image_rect)
    display.blit(text, text_rect)

    return image_rect


def handle_mouse_press(element_rect: pygame.Rect, mouse_position: tuple):
    x0, y0, width, height = element_rect
    x1 = x0 + width
    y1 = y0 + height

    if x0 <= mouse_position[0] <= x1 and y0 <= mouse_position[1] <= y1:
        return True
    else:
        return False


def initial_position():
    enemies_group.empty()
    coin_group.empty()
    config.score = 0
    config.is_died = False
    config.is_running = True

    config.is_jump = False
    config.jump_count = config.jump_count_ideal
    player_group.rect.bottomleft = (150, WORKPLACE_Y - grass_y)


pygame.init()

pygame.time.set_timer(pygame.USEREVENT, 2000)
screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
clock = pygame.time.Clock()

pause_background = pygame.image.load("sprites/menu_background.jpg").convert_alpha()

# Загружаем спрайты земли
grass_image = pygame.image.load(grass_src)
grass_x, grass_y = grass_image.get_size()
qty_of_grass = WORKPLACE_X // grass_x + 2
logger.info(f'Quantity of grass sprites - {qty_of_grass}.')
logger.info(f'The sizes of grass sprite are {grass_x}x{grass_y}')

grass_group = pygame.sprite.Group()

# Рассчитываем, сколько необходимо спрайтов земли на экран и добавляем их
initial_point = WORKPLACE_LEFT_SIDE
for i in range(0, qty_of_grass):
    Grass(initial_point + grass_x // 2,
          WINDOW_Y - grass_y // 2,
          grass_image,
          grass_group)
    initial_point += grass_x

# Загружаем спрайты игрока
player_group = Player(WORKPLACE_Y - grass_y)

# Загружаем спрайты препятствий
enemies_list = []
for i in enemies_src:
    enemies_list.append(f'sprites/enemies/{i}')
enemies_group = pygame.sprite.Group()

# Загружаем спрайты монеток
coin_group = pygame.sprite.Group()

# Загружаем спрайты цифр
number_list = []
for i in numbers_src:
    number_list.append(f'sprites/numbers/{i}')
score_group = pygame.sprite.Group()

player_count = 0


while True:
    # Координаты нажатой мыши
    coordinates_of_mouse = ()

    # Обработка событий, в том числе нажатий кнопок
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        # ------------------------ #
        # Нажатие клавишы "Escape" #
        # ------------------------ #
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Во время отображения стартового меню клавиша "Escape" не используется
            if config.is_start:
                # Ставит игру на паузу
                if config.is_running and not config.is_died:
                    config.is_pause = True
                    config.is_running = False
                    logger.info('Paused...')
                # Возобновляет игру
                elif not config.is_running and not config.is_died:
                    config.is_pause = False
                    config.is_running = True
                    logger.info('Resumed')
        # ------------------------ #
        # Нажатие клавишы "Пробел" #
        # ------------------------ #
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Во время отображения стартового меню клавиша "Пробел" не используется
            if config.is_start:
                if config.is_running and not config.is_jump:
                    config.is_jump = True
                    logger.info('Jump')
        # ------------------- #
        # Нажатие кнопок мыши #
        # ------------------- #
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Мышь используется только в меню (стартовом и паузы)
            if config.is_pause or not config.is_start or config.is_died:
                coordinates_of_mouse = event.pos
        elif event.type == pygame.USEREVENT and config.is_running:
            barrier_src = enemies_list[randint(0, len(enemies_list) - 1)]
            image_enemie = pygame.image.load(barrier_src).convert_alpha()
            Enemie(WORKPLACE_X, WORKPLACE_Y - grass_y, image_enemie, enemies_group)

            image_coin = pygame.image.load(coin_src).convert_alpha()
            Coin(WORKPLACE_X,
                 WORKPLACE_Y - grass_y - image_enemie.get_size()[1] - 100,
                 image_coin,
                 coin_group)

    # TODO Отвязать анимацию персонажа анимацию от FPS
    score_group.draw(screen)
    grass_group.draw(screen)
    screen.blit(player_group.image, player_group.rect)
    enemies_group.draw(screen)
    coin_group.draw(screen)

    # --------------------- #
    # Сцена стартового меню #
    # --------------------- #
    if not config.is_start:
        result = start_menu(coordinates_of_mouse)
        if result == 'start':
            config.is_start = True
            config.is_running = True
        elif result == 'exit':
            exit()
    # ----------- #
    # Сцена паузы #
    # ----------- #
    elif config.is_pause:
        result = pause_menu(coordinates_of_mouse)
        if result == 'resume':
            config.is_pause = False
            config.is_running = True
        elif result == 'exit':
            exit()
    # ------------ #
    # Сцена забега #
    # ------------ #
    elif config.is_running:
        if config.is_jump:
            if config.jump_count >= - config.jump_count_ideal:
                # Движение в полете. От 10 до 1 - вверх, от -1 до -9 - вниз.
                player_group.update(f'sprites/{player_jump_src}')
                config.jump_count -= 1
            else:
                # Момент приземления
                config.is_jump = False
                config.jump_count = config.jump_count_ideal
        else:
            player_group.update(f'sprites/{player_src[player_count]}')

        grass_group.update(grass_image, grass_group, grass_x, qty_of_grass, speed_of_world)
        enemies_group.update(speed_of_world)
        coin_group.update(speed_of_world)

        # Проверяем столкновение персонажа с препятствием
        hits = pygame.sprite.spritecollide(player_group, enemies_group, False)
        if hits:
            config.is_running = False
            config.is_died = True
            logger.info('Crash!!!')

            # Заменяем спрайт персонажа на погибшего
            player_group.update(f'sprites/{player_hurt_src}', config.is_running)

        # Проверяем столкновение персонажа с монеткой
        hits = pygame.sprite.spritecollide(player_group, coin_group, True)
        if hits:
            config.score += 1
            logger.info(f'Found coin! Your current result is {config.score}')
    # ---------------------- #
    # Сцена меню 'Game Over' #
    # ---------------------- #
    elif config.is_died:
        result = died_menu(coordinates_of_mouse)
        if result == 'restart':
            initial_position()
        elif result == 'exit':
            exit()

    # -------------- #
    # Update counter #
    # -------------- #
    menu_text(20, 50, f'Score: {config.score}', 24, 'left')
    menu_text(WORKPLACE_X - 20, 50, f'The best result: 35', 24, 'right')

    pygame.display.update()

    if player_count == len(player_src) - 1:
        player_count = 0
    else:
        player_count += 1

    screen.fill(BACKGROUND)
    clock.tick(40)



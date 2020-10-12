"""
Copyright 2020 Egor Vavilov (shecspi@gmail.com)
Licensed under the Apache License, Version 2.0
"""
import sqlite3
from random import randint

import pygame
from loguru import logger

import config
from coin import Coin
from modules.database import Database
from modules.scoreshowing import ScoreShowing
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
    start_rect = menu_button('sprites/green_button.png',
                             WORKPLACE_X // 2,
                             title_bottom_y + 50,
                             'Start',
                             screen)
    start_rect_y = start_rect.y + start_rect.height

    # Button "Reset"
    reset_rect = menu_button('sprites/red_button.png',
                             WORKPLACE_X // 2,
                             start_rect_y + 50,
                             'Reset',
                             screen)
    reset_rect_y = reset_rect.y + reset_rect.height

    # Button "Exit"
    exit_rect = menu_button('sprites/red_button.png',
                            WORKPLACE_X // 2,
                            reset_rect_y + 50,
                            'Exit',
                            screen)
    exit_rect_y = exit_rect.y + exit_rect.height

    # Copyright
    display_copyright(WORKPLACE_X // 2, exit_rect_y + 50)

    if pos:
        if handle_mouse_press(start_rect, pos):
            logger.info("The button 'Start' was pressed.")
            return 'start'
        elif handle_mouse_press(reset_rect, pos):
            logger.info("The button 'Reset' was pressed.")
            return 'reset'
        elif handle_mouse_press(exit_rect, pos):
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
    game_over_rect = menu_text(WORKPLACE_X // 2, 150, 'Game over', 100)
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
    config.is_record = False

    config.is_jump = False
    config.jump_count = config.jump_count_ideal
    player_group.rect.bottomleft = (150, WORKPLACE_Y - grass_y)


pygame.init()

pygame.time.set_timer(pygame.USEREVENT, 2000)
screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
clock = pygame.time.Clock()

db = Database()
# db_connect = sqlite3.connect('runner.sqlite')
# sqlite = db_connect.cursor()

pause_background = pygame.image.load("sprites/menu_background.jpg").convert_alpha()

# Download sprites of grass
grass_image = pygame.image.load(grass_src)
grass_image_first = pygame.image.load(grass_first_src)
grass_x, grass_y = grass_image.get_size()
qty_of_grass = WORKPLACE_X // grass_x + 2
logger.info(f'Quantity of grass sprites - {qty_of_grass}.')
logger.info(f'The sizes of grass sprite are {grass_x}x{grass_y}')

grass_group = pygame.sprite.Group()

# Calculation of quantity of grass sprites
initial_point = WORKPLACE_LEFT_SIDE
center_of_grass_y = WORKPLACE_Y - grass_y // 2

for i in range(0, qty_of_grass):
    Grass(initial_point + grass_x // 2,
          center_of_grass_y,
          grass_image,
          grass_group)
    initial_point += grass_x

# Download sprites of player
player_group = Player(WORKPLACE_Y - grass_y)

# Download sprites of enemies
enemies_list = []
for i in enemies_src:
    enemies_list.append(f'sprites/enemies/{i}')
enemies_group = pygame.sprite.Group()

# Download sprites of coins
coin_group = pygame.sprite.Group()

# To select sprites of player
player_count = 0

# Counter of frames for the random spawn of enemies
frame_counter = 0

# The formula for the random spawn of enemies
enemies_spawn_formula = (FPS // 2, FPS * 3)
frame_enemies_show = randint(*enemies_spawn_formula)

# The class to draw current and best results on the screen
score_showing = ScoreShowing(screen)

# The best result
best_score = db.get_best_result()
if not best_score:
    best_score = 0

cycle = True

while cycle:
    # Координаты нажатой мыши
    coordinates_of_mouse = ()

    ##############################
    # -------------------------- #
    # ----- Event handling ----- #
    # -------------------------- #
    ##############################

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cycle = False

        ##################
        # Press "Escape" #
        ##################
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Player can use the button "Escape" only on the screens "Running" and "Pause"
            if config.is_start and not config.is_died:
                # Pause
                if not config.is_pause:
                    config.is_pause = True
                    config.is_running = False
                    logger.info('Paused...')
                # Resume
                else:
                    config.is_pause = False
                    config.is_running = True
                    logger.info('Resumed')

        #################
        # Press "Space" #
        #################
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Player can jump only on screen "Running", not "Start", "Pause" and "Died"
            if config.is_start and not config.is_pause and not config.is_died:
                # There is no double jump
                if not config.is_jump:
                    config.is_jump = True
                    logger.info('Jump')

        ######################
        # Press mouse button #
        ######################
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Player can use mouse button only on the screens "Start", "Pause" and "Died"
            if not config.is_start or config.is_pause or config.is_died:
                coordinates_of_mouse = event.pos

    # TODO Отвязать анимацию персонажа анимацию от FPS
    grass_group.draw(screen)
    screen.blit(player_group.image, player_group.rect)
    enemies_group.draw(screen)
    coin_group.draw(screen)

    ###########################################
    # --------------------------------------- #
    # ----- Calculation of game screens ----- #
    # --------------------------------------- #
    ###########################################

    #######################
    # Screen "Start menu" #
    #######################
    if not config.is_start:
        result = start_menu(coordinates_of_mouse)
        if result == 'start':
            config.is_start = True
            config.is_running = True
        elif result == 'reset':
            db.reset()
            # TODO Make a beautiful animation to inform player about new record
            logger.info('Reset was made')
        elif result == 'exit':
            exit()

    ##################
    # Screen "Pause" #
    ##################
    elif config.is_pause:
        result = pause_menu(coordinates_of_mouse)
        if result == 'resume':
            config.is_pause = False
            config.is_running = True
        elif result == 'exit':
            exit()

    ####################
    # Screen "Running" #
    ####################
    elif config.is_running:
        # ---------------- #
        # Spawn of enemies #
        # ---------------- #
        if frame_counter == frame_enemies_show:
            # Spawn enemies
            enemy_src = enemies_list[randint(0, len(enemies_list) - 1)]
            image_enemy = pygame.image.load(enemy_src).convert_alpha()
            Enemie(WORKPLACE_X + grass_x // 2,
                   center_of_grass_y - grass_y // 2 - image_enemy.get_rect()[3] // 2,
                   image_enemy,
                   enemies_group)

            # Spawn coins
            image_coin = pygame.image.load(coin_src).convert_alpha()
            Coin(WORKPLACE_X + grass_x // 2,
                 center_of_grass_y - grass_y // 2 - image_enemy.get_rect()[3] // 2 - 150,
                 image_coin,
                 coin_group)

            frame_counter = 0
            frame_enemies_show = randint(*enemies_spawn_formula)
        else:
            frame_counter += 1

        # ------- #
        # Jumping #
        # ------- #
        if config.is_jump:
            # Jumping
            if config.jump_count >= - config.jump_count_ideal:
                player_group.update(f'sprites/{player_jump_src}')
                config.jump_count -= 1
            else:
                # Landing
                config.is_jump = False
                config.jump_count = config.jump_count_ideal
        else:
            player_group.update(f'sprites/{player_src[player_count]}')

        # Update sprites
        grass_group.update(grass_image,
                           grass_group,
                           grass_x,
                           qty_of_grass,
                           center_of_grass_y)
        enemies_group.update()
        coin_group.update()

        # Checking collision of character and enemies
        hit_player_enemy = pygame.sprite.spritecollide(player_group, enemies_group, False)
        hit_player_coin = pygame.sprite.spritecollide(player_group, coin_group, True)

        if hit_player_enemy:
            config.is_running = False
            config.is_died = True
            player_group.update(f'sprites/{player_hurt_src}', config.is_running)
            logger.info('Crash!!!')

        # Checking collision of character and coins
        if hit_player_coin:
            config.score += 1
            logger.info(f'Found coin! Your current result is {config.score}')

    ######################
    # Screen 'Game Over' #
    ######################
    elif config.is_died:
        if not config.is_save:
            db.insert_new_score(config.score)
            config.is_save = True

        result = died_menu(coordinates_of_mouse)
        if result == 'restart':
            initial_position()
        elif result == 'exit':
            cycle = False

    ##################
    # Update counter #
    ##################
    if config.score > best_score and not config.is_record:
        logger.info("It's a new record!!!")
        config.is_record = True
    score_showing.current_score(config.score)
    score_showing.best_score(best_score)

    pygame.display.update()

    if player_count == len(player_src) - 1:
        player_count = 0
    else:
        player_count += 1

    screen.fill(BACKGROUND)
    clock.tick(FPS)

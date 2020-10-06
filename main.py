from random import randint

import pygame
from loguru import logger

import config
from coin import Coin
from setting import *
from score import Score
from grass import Grass
from player import Player
from enemies import Enemie


def start_menu(pos):
    screen.blit(pause_background, (0, 0), None, pygame.BLEND_RGBA_SUB)

    # Надпись "Are you ready?"
    pause_font = pygame.font.Font('sprites/fonts/kenvector_future_thin.ttf', 100)
    pause_title = pause_font.render('Are you ready?', 1, (0, 0, 0))
    pause_title_rect = pause_title.get_rect(center=(WORKPLACE_X // 2, 100))
    screen.blit(pause_title, pause_title_rect)

    cloud_font = pygame.font.Font('sprites/fonts/kenvector_future_thin.ttf', 24)

    # Кнопка "Start"
    cloud_start_image = pygame.image.load('sprites/green_button.png').convert_alpha()
    cloud_start_rect = cloud_start_image.get_rect(center=(WORKPLACE_X // 2, WORKPLACE_Y // 2 - 50))
    cloud_start_text = cloud_font.render('Start', 1, (0, 0, 0))
    cloud_start_text_rect = cloud_start_text.get_rect(center=(WORKPLACE_X // 2, WORKPLACE_Y // 2 - 50))
    screen.blit(cloud_start_image, cloud_start_rect)
    screen.blit(cloud_start_text, cloud_start_text_rect)

    # Кнопка "Exit"
    cloud_exit_image = pygame.image.load('sprites/red_button.png').convert_alpha()
    cloud_exit_rect = cloud_exit_image.get_rect(center=(WORKPLACE_X // 2, WORKPLACE_Y // 2 + 50))
    cloud_exit_text = cloud_font.render('Exit', 1, (0, 0, 0))
    cloud_exit_text_rect = cloud_exit_text.get_rect(center=(WORKPLACE_X // 2, WORKPLACE_Y // 2 + 50))
    screen.blit(cloud_exit_image, cloud_exit_rect)
    screen.blit(cloud_exit_text, cloud_exit_text_rect)

    if pos:
        print(cloud_start_rect, pos)
        if handle_mouse_press(cloud_start_rect, pos):
            logger.info("The button 'Start' was pressed.")
            return 'start'
        if handle_mouse_press(cloud_exit_rect, pos):
            logger.info("The button 'Exit' was pressed.")
            return 'exit'


def pause_menu(pos):
    """
    Производит отоборажение меню паузы и производит обработку нажатия кнопок в меню.
    """
    # Отображает фоновое полупрозрачное изображение поверх сцены с игрой
    screen.blit(pause_background, (0, 0), None, pygame.BLEND_RGBA_SUB)

    # Надпись "ПАУЗА"
    pause_font = pygame.font.Font('sprites/fonts/kenvector_future_thin.ttf', 100)
    pause_title = pause_font.render('PAUSE', 1, (0, 0, 0))
    pause_title_rect = pause_title.get_rect(center=(WORKPLACE_X // 2, 100))
    screen.blit(pause_title, pause_title_rect)

    cloud_font = pygame.font.Font('sprites/fonts/kenvector_future_thin.ttf', 24)

    # Кнопка "Resume"
    cloud_resume_image = pygame.image.load('sprites/yellow_button.png').convert_alpha()
    cloud_resume_rect = cloud_resume_image.get_rect(center=(WORKPLACE_X // 2, 200))
    cloud_resume_text = cloud_font.render('Resume', 1, (0, 0, 0))
    cloud_resume_text_rect = cloud_resume_text.get_rect(center=(WORKPLACE_X // 2, 200))
    screen.blit(cloud_resume_image, cloud_resume_rect)
    screen.blit(cloud_resume_text, cloud_resume_text_rect)

    # Кнопка "Exit"
    cloud_exit_image = pygame.image.load('sprites/red_button.png').convert_alpha()
    cloud_exit_rect = cloud_exit_image.get_rect(center=(WORKPLACE_X // 2, 270))
    cloud_exit_text = cloud_font.render('Exit', 1, (0, 0, 0))
    cloud_exit_text_rect = cloud_exit_text.get_rect(center=(WORKPLACE_X // 2, 270))
    screen.blit(cloud_exit_image, cloud_exit_rect)
    screen.blit(cloud_exit_text, cloud_exit_text_rect)

    if pos:
        if handle_mouse_press(cloud_resume_rect, pos):
            logger.info("The button 'Resume' was pressed.")
            return 'resume'
        if handle_mouse_press(cloud_exit_rect, pos):
            logger.info("The button 'Exit' was pressed.")
            return 'exit'


def died_menu(pos):
    screen.blit(pause_background, (0, 0), None, pygame.BLEND_RGBA_SUB)

    # Надпись "Game over?"
    died_font = pygame.font.Font('sprites/fonts/kenvector_future_thin.ttf', 100)
    died_title = died_font.render('Game over', 1, (0, 0, 0))
    died_title_rect = died_title.get_rect(center=(WORKPLACE_X // 2, 100))
    screen.blit(died_title, died_title_rect)

    # Кнопка "Restart"
    restart_rect = menu_button('sprites/green_button.png', WORKPLACE_X // 2, WORKPLACE_Y // 2 - 50, 'Restart', screen)

    # Кнопка "Exit"
    exit_rect = menu_button('sprites/red_button.png', WORKPLACE_X // 2, WORKPLACE_Y // 2 + 50, 'Exit', screen)

    if pos:
        if handle_mouse_press(restart_rect, pos):
            logger.info("The button 'Restart' was pressed.")
            return 'restart'
        if handle_mouse_press(exit_rect, pos):
            logger.info("The button 'Exit' was pressed.")
            return 'exit'


def menu_button(image_src, x, y, message, display):
    font = pygame.font.Font('sprites/fonts/kenvector_future_thin.ttf', 24)

    image = pygame.image.load(image_src).convert_alpha()
    image_rect = image.get_rect(center=(x, y))
    text = font.render(message, 1, (0, 0, 0))
    text_rect = text.get_rect(center=(x, y))

    display.blit(image, image_rect)
    display.blit(text, text_rect)

    return image_rect


def handle_mouse_press(element_rect, mouse_position):
    x0, y0, width, height = element_rect
    x1 = x0 + width
    y1 = y0 + height

    if x0 <= mouse_position[0] <= x1 and y0 <= mouse_position[1] <= y1:
        return True
    else:
        return False


def scores_update(score, screen):
    score_font = pygame.font.Font('sprites/fonts/kenvector_future_thin.ttf', 24)
    score_text = score_font.render(f'Score: {score}', 1, (0, 0, 0))
    score_text_rect = score_text.get_rect(bottomleft=(20, 50))
    screen.blit(score_text, score_text_rect)


def best_result(score, screen):
    score_font = pygame.font.Font('sprites/fonts/kenvector_future_thin.ttf', 24)
    score_text = score_font.render(f'The best result: {score}', 1, (0, 0, 0))
    score_text_rect = score_text.get_rect(bottomright=(WORKPLACE_X - 20, 50))
    screen.blit(score_text, score_text_rect)


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

    scores_update(config.score, screen)
    best_result(35, screen)
    pygame.display.update()

    if player_count == len(player_src) - 1:
        player_count = 0
    else:
        player_count += 1

    screen.fill(BACKGROUND)
    clock.tick(40)



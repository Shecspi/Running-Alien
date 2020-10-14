"""
Copyright 2020 Egor Vavilov (shecspi@gmail.com)
Licensed under the Apache License, Version 2.0

"""

import os
from random import randint

import pygame
from loguru import logger

import config
from cloud import Cloud
from coin import Coin
from modules.ScreenMenu import ScreenMenu
from modules.database import Database
from modules.Score import Score
from setting import *
from grass import Grass
from player import Player
from enemies import Enemy


# TODO Избавиться от обращения к глобальным переменным, таких как 'screen'


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
screen_menu = ScreenMenu(screen)

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

# Download sprites of clouds
clouds_list = os.listdir(resources_dir_cloud)
clouds_group = pygame.sprite.Group()

# The formula for the random spawn of enemies
clouds_spawn_formula = (FPS // 2, FPS * 1.5)
frame_clouds_show = randint(*clouds_spawn_formula)

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
score_showing = Score(screen)

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
    clouds_group.draw(screen)
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
        result = screen_menu.display_start_menu(coordinates_of_mouse)
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
        result = screen_menu.display_pause_menu(coordinates_of_mouse)
        if result == 'resume':
            config.is_pause = False
            config.is_running = True
        elif result == 'exit':
            exit()

    ####################
    # Screen "Running" #
    ####################
    elif config.is_running:
        # ------------------ #
        # Spawn of resources #
        # ------------------ #
        if frame_counter == frame_clouds_show:
            # Spawn clouds
            cloud_src = resources_dir_cloud + clouds_list[randint(0, len(clouds_list) - 1)]
            cloud_image = pygame.image.load(cloud_src).convert_alpha()
            Cloud(WORKPLACE_X + grass_x // 2,
                  randint(100, 300),
                  cloud_image,
                  clouds_group)

        if frame_counter == frame_enemies_show:
            # Spawn enemies
            enemy_src = enemies_list[randint(0, len(enemies_list) - 1)]
            image_enemy = pygame.image.load(enemy_src).convert_alpha()
            Enemy(WORKPLACE_X + grass_x // 2,
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
        clouds_group.update()

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

        result = screen_menu.display_death_menu(coordinates_of_mouse)
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
    score_showing.display_current_score(config.score)
    score_showing.display_best_score(best_score)

    pygame.display.update()

    if player_count == len(player_src) - 1:
        player_count = 0
    else:
        player_count += 1

    screen.fill(BACKGROUND)
    clock.tick(FPS)

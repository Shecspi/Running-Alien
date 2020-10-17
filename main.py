#  Running Alien v.0.2
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

import os
from random import randint

import pygame
from loguru import logger

import config
from modules.Coin import Coin
from modules.Cloud import Cloud
from modules.Score import Score
from modules.Database import Database
from modules.ScreenMenu import ScreenMenu
from modules.SpecialEnemies import SpecialEnemy
from setting import *
from modules.Grass import Grass
from modules.Player import Player
from modules.Enemies import Enemy


# TODO Избавиться от обращения к глобальным переменным, таких как 'screen'


def initial_position():
    enemies_group.empty()
    coin_group.empty()
    score.set_current_score(0)
    config.is_died = False
    config.is_running = True
    config.is_record = False

    config.is_jump = False
    config.jump_count = config.jump_count_ideal
    player_group.rect.bottomleft = (150, screen_height - grass_y)


pygame.init()

pygame.time.set_timer(pygame.USEREVENT, 2000)
screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
screen_width, screen_height = screen.get_rect()[2:4]
clock = pygame.time.Clock()

db = Database()
screen_menu = ScreenMenu(screen, font_source, buttons_source)

# Download sprites of grass
grass_image = pygame.image.load(resources_dir_grass + grass_base_src)
grass_x, grass_y = grass_image.get_size()
qty_of_grass = screen_width // grass_x + 2

grass_group = pygame.sprite.Group()

# Calculation of quantity of grass sprites
initial_point = 0
center_of_grass_y = screen_height - grass_y // 2

for i in range(0, qty_of_grass):
    Grass(initial_point + grass_x // 2,
          center_of_grass_y,
          grass_image,
          grass_group)
    initial_point += grass_x

# Download sprites of running player
# To make correct animation the files of running player should have the following names:
#  ...1.png for first frame, ...2.png for second frame etc.
player_run_list = sorted(os.listdir(resources_dir_player_run))

# Use a random picture for jump player
player_jump_list = os.listdir(resources_dir_player_jump)

# Use a random picture for stand player
player_stand_list = os.listdir(resources_dir_player_stand)
player_stand_src = resources_dir_player_stand + player_stand_list[randint(0, len(player_stand_list) - 1)]
player_stand_image = pygame.image.load(player_stand_src).convert_alpha()

# Use a random picture for hurt player
player_hurt_list = os.listdir(resources_dir_player_hurt)

player_group = Player(screen_height - grass_y, player_stand_image)

# Download sprites of enemies
enemies_list = os.listdir(resources_dir_enemies)
enemies_group = pygame.sprite.Group()

# Laser
laser_group = pygame.sprite.Group()

# Download sprites of clouds
clouds_list = os.listdir(resources_dir_clouds)
clouds_group = pygame.sprite.Group()

# Download sprites of coins
coins_list = os.listdir(resources_dir_coins)
coin_group = pygame.sprite.Group()

# The formula for the random spawn of enemies
clouds_spawn_formula = (FPS // 2, FPS * 1.5)
frame_clouds_show = randint(*clouds_spawn_formula)

# To select sprites of player
player_count = 0

# Counter of frames for the random spawn of enemies
frame_counter = 0

# The formula for the random spawn of enemies
enemies_spawn_formula = (FPS // 2, FPS * 3)
frame_enemies_show = randint(*enemies_spawn_formula)

# The class to draw current and best results on the screen
score = Score(screen, font_source)

# The best result
score.best_score = db.get_best_result()

cycle = True

while cycle:
    # Coordinates of clicked mouse (left click)
    coordinates_of_mouse = ()
    is_clicked = False

    # Coordinates of current mouse position
    mouse_current_position = pygame.mouse.get_pos()

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
                    player_jump_src = player_jump_list[randint(0, len(player_jump_list) - 1)]
                    logger.info('Jump')

        ######################
        # Press mouse button #
        ######################
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Player can use mouse button only on the screens "Start", "Pause" and "Died"
            if not config.is_start or config.is_pause or config.is_died:
                coordinates_of_mouse = event.pos
                is_clicked = True

    # TODO Отвязать анимацию персонажа анимацию от FPS
    clouds_group.draw(screen)
    grass_group.draw(screen)
    screen.blit(player_group.image, player_group.rect)
    enemies_group.draw(screen)
    laser_group.draw(screen)
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
        result = screen_menu.display_start_menu(mouse_current_position, is_clicked)
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
        result = screen_menu.display_pause_menu(mouse_current_position, is_clicked)
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
            cloud_src = resources_dir_clouds + clouds_list[randint(0, len(clouds_list) - 1)]
            cloud_image = pygame.image.load(cloud_src).convert_alpha()
            Cloud(screen_width + grass_x // 2,
                  randint(100, 300),
                  cloud_image,
                  clouds_group)

        if frame_counter == frame_enemies_show:
            # Spawn enemies
            if randint(1, 10) == 1:
                enemy_source = laser_source
                is_laser = True
            else:
                enemy_source = resources_dir_enemies + enemies_list[randint(0, len(enemies_list) - 1)]
                is_laser = False

            image_enemy = pygame.image.load(enemy_source).convert_alpha()
            image_enemy_x, image_enemy_y, image_enemy_width, image_enemy_height = image_enemy.get_rect()
            Enemy(screen_width + grass_x // 2,
                  center_of_grass_y - grass_y // 2 - image_enemy_height // 2,
                  image_enemy,
                  enemies_group)

            if is_laser:
                image_laser_line = pygame.image.load(laser_line_source).convert_alpha()
                SpecialEnemy(screen_width + grass_x // 2 - image_enemy_width,
                             center_of_grass_y - grass_y // 2 - image_enemy_height // 2,
                             image_laser_line,
                             laser_group)

            # Spawn coins
            coin_src = resources_dir_coins + coins_list[randint(0, len(coins_list) - 1)]
            image_coin = pygame.image.load(coin_src).convert_alpha()
            Coin(screen_width + grass_x // 2,
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
                player_group.update(resources_dir_player_jump + player_jump_src,
                                    config.is_running,
                                    config.is_jump,
                                    config.jump_count)
                config.jump_count -= 1
            else:
                # Landing
                config.is_jump = False
                config.jump_count = config.jump_count_ideal

                player_src = resources_dir_player_run + player_run_list[player_count]
                player_group.update(player_src)
        else:
            player_src = resources_dir_player_run + player_run_list[player_count]
            player_group.update(player_src)

        # Update sprites
        grass_group.update(grass_image,
                           grass_group,
                           grass_x,
                           qty_of_grass,
                           center_of_grass_y,
                           speed_of_world)
        enemies_group.update(speed_of_world)
        laser_group.update(speed_of_world)
        coin_group.update(speed_of_world)
        clouds_group.update(speed_of_world)

        # Checking collision of character and enemies
        hit_player_enemy = pygame.sprite.spritecollide(player_group, enemies_group, False)
        hit_player_coin = pygame.sprite.spritecollide(player_group, coin_group, True)

        if hit_player_enemy:
            config.is_running = False
            config.is_died = True
            player_hurt_src = resources_dir_player_hurt + player_hurt_list[randint(0, len(player_hurt_list) - 1)]
            player_group.update(player_hurt_src)
            logger.info('Crash!!!')

        # Checking collision of character and coins
        if hit_player_coin:
            score.set_current_score(score.get_current_score() + 1)
            logger.info(f'Found coin! Your current result is {score.get_current_score()}')

    ######################
    # Screen 'Game Over' #
    ######################
    elif config.is_died:
        if not config.is_save:
            db.insert_new_score(score.get_current_score())
            config.is_save = True

        result = screen_menu.display_death_menu(mouse_current_position, is_clicked)
        if result == 'restart':
            score.set_best_score(score.get_current_score())
            initial_position()
        elif result == 'exit':
            cycle = False

    ##################
    # Update counter #
    ##################
    if score.get_current_score() > score.get_best_score() and not config.is_record:
        logger.info("It's a new record!!!")
        config.is_record = True
    score.display_current_score()
    score.display_best_score()

    pygame.display.update()

    if player_count == len(player_run_list) - 1:
        player_count = 0
    else:
        player_count += 1

    screen.fill(BACKGROUND)
    clock.tick(FPS)

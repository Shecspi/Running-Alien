#  Running Alien v.0.
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

from random import randint

import pygame
from loguru import logger

from modules.Coin import Coin
from modules.Cloud import Cloud
from modules.Database import Database
from modules.Grass import Grass
from modules.Enemies import Enemy
from modules.Player import Player
from modules.Score import Score
from modules.ScreenMenu import ScreenMenu
from modules.Setting import Setting
from modules.SpecialEnemies import LaserLinelEnemy
from modules.Sprite import Sprite


# TODO Избавиться от обращения к глобальным переменным, таких как 'screen'

db = Database()
setting = Setting()
sprite = Sprite()

pygame.init()

pygame.time.set_timer(pygame.USEREVENT, 2000)
screen = pygame.display.set_mode((setting.get_window_width(), setting.get_window_height()))
screen_width, screen_height = screen.get_rect()[2:4]
clock = pygame.time.Clock()

screen_menu = ScreenMenu(screen, sprite)

# Initializations of sprites of grass
grass_image = pygame.image.load(sprite.get_platform_grass())
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

# Use a random picture for stand player
player_stand_image = pygame.image.load(sprite.get_random_player_stand()).convert_alpha()
player_group = Player(screen_height - grass_y, player_stand_image)

# Initialization of enemy's group
enemies_group = pygame.sprite.Group()

# Initialization of laser line's group
laser_line_group = pygame.sprite.Group()

# Initialization of cloud's group
clouds_group = pygame.sprite.Group()

# Initialization of coin's groups
coin_regular_group = pygame.sprite.Group()
coin_laser_group = pygame.sprite.Group()

# The formula for the random spawn of enemies
clouds_spawn_formula = (setting.get_fps() // 2, setting.get_fps() * 1.5)
frame_clouds_show = randint(*clouds_spawn_formula)

# Counter of frames for the random spawn of enemies
frame_counter = 0

# The formula for the random spawn of enemies
enemies_spawn_formula = (setting.get_fps() // 2, setting.get_fps() * 3)
frame_enemies_show = randint(*enemies_spawn_formula)

# The class to draw current and best results on the screen
score = Score(screen, sprite.get_font())

# The best result
score.set_best_score(db.get_best_result())

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
            if setting.get_is_start() and not setting.get_is_died():
                # Pause
                if not setting.get_is_pause():
                    setting.set_is_pause(True)
                    setting.set_is_running(False)
                    logger.info('Paused...')
                # Resume
                else:
                    setting.set_is_pause(False)
                    setting.set_is_running(True)
                    logger.info('Resumed')

        #################
        # Press "Space" #
        #################
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Player can jump only on screen "Running", not "Start", "Pause" and "Died"
            if setting.get_is_start() and not setting.get_is_pause() and not setting.get_is_died():
                # There is no double jump
                if not setting.get_is_jump():
                    setting.set_is_jump(True)
                    player_jump_src = sprite.get_random_player_jump()
                    logger.info('Jump')

        ######################
        # Press mouse button #
        ######################
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Player can use mouse button only on the screens "Start", "Pause" and "Died"
            if not setting.get_is_start() or setting.get_is_pause() or setting.get_is_died():
                coordinates_of_mouse = event.pos
                is_clicked = True

    # TODO Отвязать анимацию персонажа анимацию от FPS
    clouds_group.draw(screen)
    grass_group.draw(screen)
    screen.blit(player_group.image, player_group.rect)
    enemies_group.draw(screen)
    laser_line_group.draw(screen)
    coin_regular_group.draw(screen)
    coin_laser_group.draw(screen)

    ###########################################
    # --------------------------------------- #
    # ----- Calculation of game screens ----- #
    # --------------------------------------- #
    ###########################################

    #######################
    # Screen "Start menu" #
    #######################
    if not setting.get_is_start():
        result = screen_menu.display_start_menu(mouse_current_position, is_clicked)
        if result == 'start':
            setting.set_is_start(True)
            setting.set_is_running(True)
        elif result == 'reset':
            db.reset()
            # TODO Make a beautiful animation to inform player about new record
            logger.info('Reset was made')
        elif result == 'exit':
            exit()

    ##################
    # Screen "Pause" #
    ##################
    elif setting.get_is_pause():
        result = screen_menu.display_pause_menu(mouse_current_position, is_clicked)
        if result == 'resume':
            setting.set_is_pause(False)
            setting.set_is_running(True)
        elif result == 'exit':
            exit()

    ####################
    # Screen "Running" #
    ####################
    elif setting.get_is_running():
        if frame_counter == frame_clouds_show:
            # ------------ #
            # Spawn clouds #
            # ------------ #
            cloud_src = sprite.get_random_cloud()
            cloud_image = pygame.image.load(cloud_src).convert_alpha()
            Cloud(screen_width + grass_x // 2,
                  randint(100, 300),
                  cloud_image,
                  clouds_group)

        if frame_counter == frame_enemies_show:
            # ----------------------- #
            # Spawn enemies and coins #
            # ----------------------- #
            if randint(1, 5) == 1:
                # Spawn a laser
                image_enemy = pygame.image.load(sprite.get_laser_gun()).convert_alpha()
                image_coin = pygame.image.load(sprite.get_coin_level_2()).convert_alpha()
                is_laser = True
            else:
                # Spawn a regular enemy
                enemy_source = sprite.get_random_enemy()
                image_enemy = pygame.image.load(enemy_source).convert_alpha()
                image_coin = pygame.image.load(sprite.get_coin_level_1()).convert_alpha()
                is_laser = False

            image_enemy_x, image_enemy_y, image_enemy_width, image_enemy_height = image_enemy.get_rect()
            Enemy(screen_width + grass_x // 2,
                  center_of_grass_y - grass_y // 2 - image_enemy_height // 2,
                  image_enemy,
                  enemies_group)

            if is_laser:
                # Spawn a moving laser line and a special laser coin
                image_laser_line = pygame.image.load(sprite.get_laser_line()).convert_alpha()
                LaserLinelEnemy(screen_width + grass_x // 2 - image_enemy_width,
                                center_of_grass_y - grass_y // 2 - image_enemy_height // 2,
                                image_laser_line,
                                laser_line_group)
                coin_group = coin_laser_group
            else:
                # Spawn a regular coin
                coin_group = coin_regular_group

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
        if setting.get_is_jump():
            # Jumping
            if setting.get_counter_jump() >= - setting.get_counter_initial_jump():
                player_group.update(player_jump_src,
                                    setting.get_is_running(),
                                    setting.get_is_jump(),
                                    setting.get_counter_jump())
                setting.set_counter_jump(setting.get_counter_jump() - 1)
            else:
                # Landing
                setting.set_is_jump(False)
                setting.reset_counter_jump()

                player_group.update(sprite.get_next_run_player_sprite())
        else:
            player_group.update(sprite.get_next_run_player_sprite())

        # Update sprites
        grass_group.update(grass_image,
                           grass_group,
                           grass_x,
                           qty_of_grass,
                           center_of_grass_y,
                           setting)
        enemies_group.update(setting)
        laser_line_group.update(setting)
        coin_regular_group.update(setting)
        coin_laser_group.update(setting)
        clouds_group.update(setting)

        # Checking collision of character and enemies
        hit_player_enemy = pygame.sprite.spritecollide(player_group, enemies_group, False)
        hit_player_coin = pygame.sprite.spritecollide(player_group, coin_regular_group, True)
        hit_player_lasercoin = pygame.sprite.spritecollide(player_group, coin_laser_group, True)
        hit_player_laserline = pygame.sprite.spritecollide(player_group, laser_line_group, False)

        if hit_player_enemy or hit_player_laserline:
            setting.set_is_running(False)
            setting.set_is_died(True)
            player_group.update(sprite.get_random_player_hurt())
            logger.info('Crash!!!')

        # Checking collision of character and coins
        if hit_player_coin:
            score.set_current_score(score.get_current_score() + 1)
            logger.info(f'Found a coin! Your current result is {score.get_current_score()}')

        if hit_player_lasercoin:
            score.set_current_score(score.get_current_score() + 3)
            logger.info(f'Found a laser-coin! Your current result is {score.get_current_score()}')

    ######################
    # Screen 'Game Over' #
    ######################
    elif setting.get_is_died():
        if not setting.get_is_save():
            db.insert_new_score(score.get_current_score())
            setting.set_is_save(True)

        result = screen_menu.display_death_menu(mouse_current_position, is_clicked)
        if result == 'restart':
            if score.get_current_score() > score.get_best_score():
                score.set_best_score(score.get_current_score())
            else:
                score.set_best_score(score.get_best_score())
            score.set_current_score(0)

            setting.set_is_died(False)
            setting.set_is_running(True)
            setting.set_is_record(False)
            setting.set_is_jump(False)
            setting.reset_counter_jump()

            enemies_group.empty()
            laser_line_group.empty()
            coin_regular_group.empty()
            coin_laser_group.empty()
            player_group.rect.bottomleft = (150, screen_height - grass_y)
        elif result == 'exit':
            cycle = False

    ##################
    # Update counter #
    ##################
    if score.get_current_score() > score.get_best_score() and not setting.get_is_record():
        logger.info("It's a new record!!!")
        setting.set_is_record(True)
    score.display_current_score()
    score.display_best_score()

    pygame.display.update()

    screen.fill(setting.get_color_background())
    clock.tick(setting.get_fps())

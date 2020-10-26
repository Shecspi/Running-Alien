#  Running Alien v.0.
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

from random import randint

import pygame
from loguru import logger

from modules.Block import Block
from modules.Coin import Coin
from modules.Cloud import Cloud
from modules.Database import Database
from modules.Grass import Grass
from modules.Enemies import Enemy
from modules.Heart import Heart
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
grass_width, grass_height = grass_image.get_size()
qty_of_grass = screen_width // grass_width + 2

grass_group = pygame.sprite.Group()

# Calculation of quantity of grass sprites
initial_point = 0
center_of_grass_y = screen_height - grass_height // 2
ground_line_y = center_of_grass_y - grass_height // 2

for i in range(0, qty_of_grass):
    Grass(initial_point + grass_width // 2,
          center_of_grass_y,
          grass_image,
          grass_group)
    initial_point += grass_width

# Use a random picture for stand player
player_group = Player(screen_height - grass_height, sprite)

# Initialization of enemy's group
enemies_group = pygame.sprite.Group()

blocks_group = pygame.sprite.Group()

# Initialization of laser line's group
laser_line_group = pygame.sprite.Group()

# Initialization of cloud's group
clouds_group = pygame.sprite.Group()

# Initialization of heart's group
heart_group = pygame.sprite.Group()

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

blocks_spawn_formula = (setting.get_fps() // 2, setting.get_fps() * 2)
frame_counter_blocks = randint(*blocks_spawn_formula)

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
    blocks_group.draw(screen)
    grass_group.draw(screen)
    screen.blit(player_group.image, player_group.rect)
    enemies_group.draw(screen)
    laser_line_group.draw(screen)
    coin_regular_group.draw(screen)
    coin_laser_group.draw(screen)
    heart_group.draw(screen)

    ###########################################
    # --------------------------------------- #
    # ----- Calculation of game screens ----- #
    # --------------------------------------- #
    ###########################################

    # Display the heart on the screen
    image_heart = pygame.image.load(sprite.get_heart()).convert_alpha()
    heart_x = screen_width - 70
    for i in range(0, setting.get_qty_of_lives_current()):
        Heart(heart_x,
              30,
              image_heart,
              heart_group)
        heart_x -= image_heart.get_size()[0] - 15

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
            Cloud(screen_width + grass_width // 2,
                  randint(100, 300),
                  cloud_image,
                  clouds_group)

        # if frame_counter == frame_counter_blocks:
        #     image_block = pygame.image.load(sprite.get_random_block()).convert_alpha()
        #     Block(screen_width + grass_x // 2,
        #           screen_height - 200,
        #           image_block,
        #           blocks_group)

        if frame_counter == frame_enemies_show:
            # ----------------------- #
            # Spawn enemies and coins #
            # ----------------------- #
            is_laser = True if randint(1, 5) == 1 else False
            coin_group = coin_laser_group if is_laser else coin_regular_group

            enemy = Enemy(setting.get_window_width() + grass_width // 2,
                          ground_line_y,
                          sprite,
                          enemies_group,
                          is_laser)

            Coin(setting.get_window_width() + grass_width // 2,
                 ground_line_y - enemy.get_height() - 150,
                 sprite,
                 coin_group,
                 is_laser)

            frame_counter = 0
            frame_enemies_show = randint(*enemies_spawn_formula)
        else:
            frame_counter += 1

        # Update sprites
        grass_group.update(grass_image,
                           grass_group,
                           grass_width,
                           qty_of_grass,
                           center_of_grass_y,
                           setting)
        blocks_group.update(setting)
        enemies_group.update(setting)
        laser_line_group.update(setting)
        coin_regular_group.update(setting)
        coin_laser_group.update(setting)
        clouds_group.update(setting)

        all_groups = {
            'enemies': enemies_group,
            'coin_regular': coin_regular_group,
            'coin_laser': coin_laser_group,
            'laser_line': laser_line_group
        }
        kill_instance = {
            'enemies': False,
            'coin_regular': True,
            'coin_laser': True,
            'laser_line': False
        }
        hit = player_group.update(setting, sprite, all_groups, kill_instance)

        # Checking collision of character and enemies
        if hit == 'enemies':
            setting.set_is_running(False)
            setting.set_is_died(True)
        elif hit == 'laser_line':
            pass
        elif hit == 'coin_regular':
            score.set_current_score(score.get_current_score() + 1)
            logger.info(f'Found a coin! Your current result is {score.get_current_score()}')
        elif hit == 'coin_laser':
            score.set_current_score(score.get_current_score() + 3)
            logger.info(f'Found a laser-coin! Your current result is {score.get_current_score()}')

    ######################
    # Screen 'Game Over' #
    ######################
    elif setting.get_is_died():
        if not setting.get_is_save():
            db.insert_new_score(score.get_current_score())
            setting.set_qty_of_lives_current(setting.get_qty_of_lives_current() - 1)
            heart_group.empty()
            setting.set_is_save(True)

        result = screen_menu.display_death_menu(mouse_current_position, is_clicked, setting.get_qty_of_lives_current())

        if result == 'exit':
            cycle = False
        elif result == 'restart' or result == 'next_life':
            setting.set_is_died(False)
            setting.set_is_running(True)
            setting.set_is_record(False)
            setting.set_is_jump(False)
            setting.reset_counter_jump()
            setting.set_is_save(False)

            enemies_group.empty()
            laser_line_group.empty()
            coin_regular_group.empty()
            coin_laser_group.empty()
            player_group.rect.bottomleft = (150, screen_height - grass_height)

        if result == 'restart':
            if score.get_current_score() > score.get_best_score():
                score.set_best_score(score.get_current_score())
            else:
                score.set_best_score(score.get_best_score())
            score.set_current_score(0)
            setting.set_qty_of_lives_current(setting.get_qty_of_lives_default())

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

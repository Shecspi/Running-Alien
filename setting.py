#  Running Alien v.0.2
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

# Размеры экрана
WINDOW_Y = 600
WINDOW_X = 1000

# Размеры игровой зоны
WORKPLACE_Y = 600
WORKPLACE_X = 1000
WORKPLACE_LEFT_SIDE = (WINDOW_X - WORKPLACE_X) // 2
WORKPLACE_RIGHT_SIDE = WINDOW_X - WORKPLACE_LEFT_SIDE

FPS = 40

speed_of_world = 10

WHITE = (255, 255, 255)
BACKGROUND = (135, 206, 235)

grass_base_src = 'grass_base.png'

resources_dir_grass = 'resources/sprites/grass/'
resources_dir_clouds = 'resources/sprites/clouds/'
resources_dir_enemies = 'resources/sprites/enemies/'
resources_dir_coins = 'resources/sprites/coins/'
resources_dir_player_stand = 'resources/sprites/player/stand/'
resources_dir_player_run = 'resources/sprites/player/run/'
resources_dir_player_jump = 'resources/sprites/player/jump/'
resources_dir_player_hurt = 'resources/sprites/player/hurt/'

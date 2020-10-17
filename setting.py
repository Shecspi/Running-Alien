#  Running Alien v.0.2
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

# Size of screen
WINDOW_Y = 600
WINDOW_X = 1000

FPS = 40

# Speed of the world moving
speed_of_world = 10

WHITE = (255, 255, 255)
BACKGROUND = (135, 206, 235)

grass_base_src = 'grass_base.png'
font_source = 'resources/fonts/Chilanka-Regular.ttf'

# Directories with resources
resources_dir_grass = 'resources/sprites/grass/'
resources_dir_clouds = 'resources/sprites/clouds/'
resources_dir_enemies = 'resources/sprites/enemies/'
resources_dir_coins = 'resources/sprites/coins/'
resources_dir_player_stand = 'resources/sprites/player/stand/'
resources_dir_player_run = 'resources/sprites/player/run/'
resources_dir_player_jump = 'resources/sprites/player/jump/'
resources_dir_player_hurt = 'resources/sprites/player/hurt/'
resources_dir_button = 'resources/buttons/'

buttons_source = {
    'green': resources_dir_button + 'green_button.png',
    'green_shadow': resources_dir_button + 'green_shadow_button.png',
    'red': resources_dir_button + 'red_button.png',
    'red_shadow': resources_dir_button + 'red_shadow_button.png',
    'yellow': resources_dir_button + 'yellow_button.png',
    'yellow_shadow': resources_dir_button + 'yellow_shadow_button.png'
}

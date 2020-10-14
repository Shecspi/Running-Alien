"""
Copyright 2020 Egor Vavilov (shecspi@gmail.com)
Licensed under the Apache License, Version 2.0
"""

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

grass_src = 'grassMid.png'
grass_first_src = 'sprites/grass_first.png'

player_src = ['p3_walk01.png', 'p3_walk02.png', 'p3_walk03.png', 'p3_walk04.png',
              'p3_walk05.png', 'p3_walk06.png', 'p3_walk07.png', 'p3_walk08.png',
              'p3_walk09.png', 'p3_walk10.png', 'p3_walk11.png']
player_jump_src = 'p3_jump.png'
player_down_src = 'sprites/player/down.png'
player_hurt_src = 'p3_hurt.png'

enemies_src = ['pokerMad.png', 'cactus.png', 'snailWalk1.png']

resources_dir_cloud = 'resources/sprites/clouds/'

numbers_src = ['0.png', '1.png', '2.png', '3.png', '4.png',
               '5.png', '6.png', '7.png', '8.png', '9.png']

coin_src = 'sprites/coin.png'

coin_sound_src = 'sounds/coin.ogg'

"""
Copyright 2020 Egor Vavilov (shecspi@gmail.com)
Licensed under the Apache License, Version 2.0
"""

is_running = True  # Бежит ли персонаж
is_start = False  # Запущен ли игровой процесс
is_pause = False  # Поставлена ли игра на паузу
is_died = False  # Погиб ли персонаж
is_jump = False

score = 0
jump_count = jump_count_ideal = 10
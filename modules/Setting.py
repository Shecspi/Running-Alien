#  Running Alien v. 0.2
#
#  Copyright © 2020 Egor Vavilov (shecspi@gmail.com)
#  Licensed under the Apache License, Version 2.0

""" Setting management module.

It includes the methods to get and to set any settings.

The module sets default values of setting when initializing a class.
To reset setting you should kill a current instance and create new one.

"""


class Setting:
    def __init__(self):
        self.__is_died: bool = False
        self.__is_jump: bool = False
        self.__is_pause: bool = False
        self.__is_record: bool = False
        self.__is_running: bool = False
        self.__is_save: bool = False
        self.__is_start: bool = False

        self.__counter_jump: int = 10
        self.__counter_initial_jump: int = 10

        self.__fps: int = 40  # Frames per a second
        self.__speed_of_world: int = 10  # Speed of moving the world

    def get_counter_jump(self) -> int:
        return self.__counter_jump

    def set_counter_jump(self, count: int) -> None:
        self.__counter_jump = count

    def get_counter_initial_jump(self):
        return self.__counter_initial_jump

    def reset_counter_jump(self):
        self.__counter_jump = self.__counter_initial_jump

    def get_is_died(self) -> bool:
        return self.__is_died

    def set_is_died(self, is_died: bool) -> None:
        self.__is_died = is_died

    def get_is_jump(self) -> bool:
        return self.__is_jump

    def set_is_jump(self, is_jump: bool) -> None:
        self.__is_jump = is_jump

    def get_is_pause(self) -> bool:
        return self.__is_pause

    def set_is_pause(self, is_pause: bool) -> None:
        self.__is_pause = is_pause

    def get_is_record(self) -> bool:
        return self.__is_record

    def set_is_record(self, is_record: bool) -> None:
        self.__is_record = is_record

    def get_is_running(self) -> bool:
        return self.__is_running

    def set_is_running(self, is_running: bool) -> None:
        self.__is_running = is_running

    def get_is_save(self) -> bool:
        return self.__is_save

    def set_is_save(self, is_save: bool) -> None:
        self.__is_save = is_save

    def get_is_start(self) -> bool:
        return self.__is_start

    def set_is_start(self, is_start: bool) -> None:
        self.__is_start = is_start

    def get_fps(self) -> int:
        return self.__fps

    def set_fps(self, fps: int) -> None:
        self.__fps = fps

    def get_speed_of_world(self) -> int:
        return self.__speed_of_world

    def set_speed_of_world(self, speed: int) -> None:
        self.__speed_of_world = speed

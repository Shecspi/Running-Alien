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
        # Speed of moving the world
        self.__speed_of_world: int = 10

    def get_speed_of_world(self) -> int:
        return self.__speed_of_world

    def set_speed_of_world(self, speed: int) -> None:
        self.__speed_of_world = speed

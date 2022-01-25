from random import choice, randint
from typing import Tuple

import pygame
from pygame import Rect, Surface

from constants import BLOCK, Colors
from utils import get_randon_position


def random_color():
    return (randint(50, 255), randint(50, 255), randint(50, 255))


class Thiago:
    """Manage square objects over a 2D screen"""

    def __init__(
        self, x: int, y: int, width: int, height: int, color: Tuple[int]
    ) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def __get_color(self):
        return random_color() if self.color == Colors.RANDOM else self.color

    def update(self, screen: Surface) -> Rect:
        return pygame.draw.rect(
            screen,
            self.__get_color(),
            (self.x, self.y, self.width, self.height)
        )

# herança
class Food(Thiago):
    points = 1
    color = Colors.GREEN
    width = BLOCK
    height = BLOCK

    def __init__(
        self, x: int,
        y: int
    ) -> None:
        super().__init__(x, y, self.width, self.height, color=self.color)


class SpecialFood(Food):
    points = 10
    color = Colors.RANDOM


class FoodController:
    def __init__(self) -> None:
        self.food = self.__get_food()

    def __get_food(self) -> Food:
        pos = get_randon_position()
        return choice([Food(*pos), SpecialFood(*pos)])

    def renew(self):
        self.food = self.__get_food()

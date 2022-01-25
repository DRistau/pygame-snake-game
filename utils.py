from random import choice, randint
from typing import Tuple

from constants import BLOCK, W_HEIGHT, W_WIDTH


def random_color() -> Tuple[int]:
    """Returns a random RGB color as tuple."""
    return (randint(50, 255), randint(50, 255), randint(50, 255))


def get_randon_position() -> Tuple[int]:
    """Returns a random 2D position from the board."""
    x_spots = range(0, W_WIDTH, BLOCK)
    y_spots = range(0, W_HEIGHT, BLOCK)

    return (
        choice(x_spots),
        choice(y_spots),
    )

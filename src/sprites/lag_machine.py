"""A module for working with lag machine.

The lag machine calculates the pi number, and updates each frame, which heavily loads the application.
"""
from typing import TYPE_CHECKING, Any, Generator
from decimal import Decimal, getcontext

import pygame as pg
from pygame import Vector2

from src.sprite import Sprite
from src.sprites import Text

if TYPE_CHECKING:
    from src.app import App


class LagMachine(Sprite):
    """The class responsible for the lag machine.
    """

    def __init__(self, app: 'App', position: Vector2):
        """Initialization.

        Args:
            app: The main class of the application.
            position: The position of the sprite on the screen.
        """
        super().__init__(app, (50, 50), position)
        self._calculation_generator = self._calculate_harmonic_series()

    def update_view(self):
        self.image.fill((32, 32, 32))

        text: Text = Text(self.app, Vector2(25, 25), next(self._calculation_generator))
        self.image.blit(text.image, text.position)

        pg.draw.rect(self.image, (78, 78, 78), pg.Rect(
            0, 0, self.image.get_size()[0], self.image.get_size()[1]
        ), 3)

    async def update(self):
        self.update_view()

    @staticmethod
    def _calculate_harmonic_series() -> Generator[str, Any, None]:
        sum_val = 0.0
        i = 1
        while True:
            sum_val += 1.0 / i
            i += 1
            yield str(sum_val)[-1:][0]

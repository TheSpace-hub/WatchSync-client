"""The module that adds the wait sprite.
"""
import time
from typing import TYPE_CHECKING, cast, Self
from math import sin, cos
from enum import Enum

import pygame as pg

from pygame import Vector2

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.app import App


class CompletionStatus(Enum):
    """Completion or work status.
    """
    WORKING = (78, 78, 78)
    HOLD = (157, 157, 157)
    SUCCESS = (0, 200, 0)
    ATTENTION = (200, 200, 0)
    ERROR = (200, 0, 0)

    @property
    def value(self) -> tuple[int, int, int]:
        return cast(tuple[int, int, int], super().value)

    @classmethod
    def get_status_by_response_status_code(cls, code: int) -> Self:
        """Get CompletionStatus based on the response status of the service.

        Raises:
            ValueError: If the code is not an http code.
        """
        if 200 <= code <= 299:
            return CompletionStatus.SUCCESS
        elif 100 <= code <= 199 or 300 <= code <= 399 or 400 <= code <= 499:
            return CompletionStatus.ATTENTION
        elif 500 <= code <= 599:
            return CompletionStatus.ERROR
        raise ValueError


class Waiting(Sprite):
    """Sprite class for waiting for something.

    Attributes:
        completion_status: Completion or work status.
    """

    def __init__(self, app: 'App', position: Vector2, size: tuple[int, int],
                 completion_status: CompletionStatus = CompletionStatus.WORKING):
        """Initialization.

        Args:
            app: The main class of the application.
            position: The position of the sprite on the screen.
            size: Sprite scale.
            completion_status: Completion or work status.
        """
        super().__init__(app, size, position)
        self.completion_status: CompletionStatus = completion_status

    def update_view(self):
        self.image.fill((32, 32, 32))

        if self.completion_status == CompletionStatus.WORKING:
            self._update_loading_plate()
        else:
            self.image.fill(list(map(lambda c: max(0, c - 125), self.completion_status.value)))

        pg.draw.rect(self.image, self.completion_status.value, pg.Rect(
            0, 0, self.image.get_size()[0], self.image.get_size()[1]
        ), 3)

    async def update(self):
        self.update_view()

    def _update_loading_plate(self):
        """Animation implementation for the loading plate.
        """

        def get_dimensions_of_loading_plate() -> tuple[float, float]:
            """Gets the width coordinate [-1; 1] of the animated element depending on the time.

            Returns:
                Tuple with start and end coordinates [-1; 1].
            """
            return sin(time.time() * 1.5), cos(time.time() * 1.5)

        dimensions_of_loading_plate: tuple[float, float] = get_dimensions_of_loading_plate()

        pg.draw.line(self.image, (255, 255, 255),
                     [
                         self.image.get_size()[0] * (dimensions_of_loading_plate[0] + 1) / 2,
                         self.image.get_size()[1] / 2
                     ],
                     [
                         self.image.get_size()[0] * (dimensions_of_loading_plate[1] + 1) / 2,
                         self.image.get_size()[1] / 2
                     ], self.image.get_size()[1])

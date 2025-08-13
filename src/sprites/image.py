"""The module that adds the image.
"""
from typing import TYPE_CHECKING, Self

import pygame as pg
from pygame import Vector2

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.app import App


class Image(Sprite):
    """Sprite class for loading and displaying images.

    Attributes:
        _origin: The original image is unchanged.
        _scale: Current image scale
        _angle: The current tilt of the image in degrees.
    """

    def __init__(self, app: 'App', position: Vector2, path: str, scale: tuple[int, int] | None = None):
        """Initialization.

        Args:
            app: The main class of the application.
            position: The position of the sprite on the screen.
            path: The path to the image.
            scale: Image scale.
        """
        super().__init__(app, (0, 0), position)
        self._origin = pg.image.load(path)
        self.image = self._origin.copy()

        self._scale: tuple[int, int] = self.image.get_size()
        self._angle: float = 0

        if scale is not None:
            self.change_scale(scale)

    def change_scale(self, scale: tuple[int, int]) -> Self:
        """Change the image scale.

        Args:
            scale: New image scale.

        Returns:
            The image itself.
        """
        self._scale = scale
        self.image = pg.transform.scale(self._origin, scale)
        return self

    def rotate(self, angle: float) -> Self:
        """Flip the image.

        Args:
            angle: Angle of rotation in degrees.

        Returns:
            The image itself.
        """
        self._angle = angle
        self.image = pg.transform.rotate(pg.transform.scale(self._origin, self._scale), angle)
        return self

    def get_angle(self) -> float:
        """Get the angle of the image.

        Returns:
            The angle of the image
        """
        return self._angle

    def update_view(self):
        pass

    async def update(self):
        pass

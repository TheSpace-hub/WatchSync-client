"""A module for working with game sprites. Provides basic functionality.
"""

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from pygame import Surface, sprite, Rect, SRCALPHA, Vector2

if TYPE_CHECKING:
    from src.app import App


class Sprite(sprite.Sprite, ABC):
    """An abstract base class for game sprites.

    Attributes:
        app (App): The main class of the application.
        image (Surface): Graphical representation of a sprite.
        position (Vector2): Determining the sprite position.

    """

    def __init__(self, app: 'App', size: tuple[int, int], position: Vector2 = Vector2(0, 0)):
        """Initializes the sprite.

        Args:
            app: Ссылка на основной игровой объект
            size: Размер спрайта в пикселях (ширина, высота)
            position: Начальная позиция спрайта (x, y). По умолчанию (0, 0)
        """
        super().__init__()
        self.app: 'App' = app
        self.image: Surface = Surface(size, SRCALPHA, 32).convert_alpha()
        self.position: Vector2 = position

    @abstractmethod
    def update_view(self):
        """Updates the graphical representation of the sprite.
        """
        self.image = Surface(self.image.get_size(), SRCALPHA, 32).convert_alpha()

    @abstractmethod
    async def update(self):
        """Updates the sprite logic. Each frame is called.
        """

"""A module that adds a button.
"""
from typing import TYPE_CHECKING, Callable, Optional, Union, Any, Coroutine

import pygame as pg
from pygame import Vector2

from src.sprites import InBlockText

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.app import App


class Button(Sprite):
    """The class that implements the button.

    Attributes:
        text: The text that is displayed on the button.
        placeholder: An image that can be inserted into the button.
        disabled: A flag indicating whether the button is working.
        callback: The function that is called when interacting with the button.
        context: The context in which the button is called. It will be passed to the function when the button is clicked.
    """

    def __init__(self, app: 'App', position: Vector2, size: tuple[int, int], text: Optional[InBlockText] = None,
                 callback: Optional[Callable[[Optional[str]], Coroutine[Any, Any, None]]] = None,
                 context: Optional[str] = None,
                 placeholder: Optional[Callable[[], pg.Surface]] = None,
                 disabled: bool = False):
        """Initialization.

        Args:
            app: The main class of the application.
            position: The position of the sprite on the screen.
            size: Button size.
            text: Displayed text.
            disabled: A flag indicating whether the button is working.
            callback: The function that is called when interacting with the button.
            context: The context in which the button is called. It will be passed to the function when the button is clicked.
            placeholder: An image that can be inserted into the button.
        """
        super().__init__(app, size, position)
        self.text: InBlockText = text
        self.placeholder: Callable[[], pg.Surface] | None = placeholder
        self.disabled: bool = disabled

        self.callback: Optional[Callable[[Optional[str]], Coroutine[Any, Any, None]]] = callback
        self.context: Optional[str] = context

        text.correct_position(size)
        self.update_view()

    def update_view(self):
        if (self.position.x <= pg.mouse.get_pos()[0] <= self.position.x + self.image.get_size()[0] and
                self.position.y <= pg.mouse.get_pos()[1] <= self.position.y + self.image.get_size()[1]):
            self.image.fill((58, 58, 58) if pg.mouse.get_pressed()[0] else (23, 23, 23))
        else:
            self.image.fill((32, 32, 32))

        self.image.blit(self.text.image, self.text.position)
        pg.draw.rect(self.image, (78, 78, 78), pg.Rect(
            0, 0, self.image.get_size()[0], self.image.get_size()[1]
        ), 3)

        if self.placeholder is not None:
            placeholder: pg.Surface = self.placeholder()
            self.image.blit(placeholder, (3, 3))

    async def update(self):
        if (self.app.is_mouse_move or self.app.omitted_mouse_buttons) and not self.disabled:
            self.update_view()

            if (self.position.x <= pg.mouse.get_pos()[0] <= self.position.x + self.image.get_size()[0] and
                    self.position.y <= pg.mouse.get_pos()[1] <= self.position.y + self.image.get_size()[1] and
                    pg.mouse.get_pressed()[0] and self.app.omitted_mouse_buttons):
                await self._call_func()

    async def _call_func(self):
        """Calling the receiving function.
        """
        if self.callback is not None:
            await self.callback(self.context)

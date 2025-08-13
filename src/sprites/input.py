from typing import TYPE_CHECKING, Optional, Self, Callable
from enum import Enum

import pygame as pg
from pygame import Vector2

from src.sprites import TextSettings, InBlockText

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.app import App


class InputFormatting(Enum):
    NO_FORMATTING = 0
    ONLY_DIGITS = 1
    NORMALIZED = 2

    @classmethod
    def formatting(cls, formatting: Self, line: str) -> str:
        """Formatting line.

        Returns:
            Formatted string.
        """
        action: dict[Self, Callable[[chr], chr]] = {
            InputFormatting.NO_FORMATTING: lambda s: s,
            InputFormatting.ONLY_DIGITS: lambda s: s if 48 <= ord(s) <= 57 else '',
            InputFormatting.NORMALIZED: lambda s: '_' if s == ' ' else s.lower()
        }
        new_line: str = ''
        for symbol in line:
            new_line += action[formatting](symbol)

        return new_line


class Input(Sprite):
    def __init__(self, app: 'App', position: Vector2, size: tuple[int, int], text: TextSettings,
                 placeholder: Optional[InBlockText], formatting: InputFormatting = InputFormatting.NO_FORMATTING,
                 default: str = '', limit: int = 0, disabled: bool = False):
        """Initialization.

        Args:
            app: The main class of the application.
            position: The position of the sprite on the screen.
            size: Input size.
            text: Displayed text.
            placeholder: The text that is displayed instead of the void.
            formatting: Text formatting.
            default: The default string.
            limit: Character limit.
            disabled: Disable flag.
        """
        super().__init__(app, size, position)
        self.text: TextSettings = text
        self.placeholder: Optional[InBlockText] = placeholder

        self.limit: int = limit
        self.formatting: InputFormatting = formatting
        self.disabled: bool = disabled

        self.selected: bool = False

        self.text.text = default

        text.correct_position(size)
        placeholder.correct_position(size)

        self.text.update_view()
        self.update_view()

    def update_view(self):
        self.text.correct_position((self.image.get_size()[0], self.image.get_size()[1]))
        self.text.update_view()

        self.image.fill((58, 58, 58) if self.selected or self.disabled else (32, 32, 32))

        self.image.blit(self.placeholder.image if self.text.text == '' else self.text.image,
                        self.placeholder.position if self.text.text == '' else self.text.position)

        pg.draw.rect(self.image, (78, 78, 78), pg.Rect(
            0, 0, self.image.get_size()[0], self.image.get_size()[1]
        ), 3)

    async def update(self):
        if 1 in self.app.omitted_mouse_buttons:
            self.selected = (self.position.x <= pg.mouse.get_pos()[0] <= self.position.x + self.image.get_size()[0] and
                             self.position.y <= pg.mouse.get_pos()[1] <= self.position.y + self.image.get_size()[1])
            self.update_view()

        if self.selected:
            for key in self.app.omitted_buttons:
                if 32 <= key <= 126 and not self.disabled and (len(self.text.text) < self.limit or self.limit <= 0):
                    self.text.text = InputFormatting.formatting(self.formatting, self.text.text + chr(key))
                    self.update_view()
                if key == 8:
                    self.text.text = self.text.text[:-1]
                    self.update_view()

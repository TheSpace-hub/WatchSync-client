"""A module for working with text.
"""
import os.path
from typing import TYPE_CHECKING, Optional, Self
from enum import Enum

import pygame as pg
from pygame import SRCALPHA, Vector2

from src.sprite import Sprite

if TYPE_CHECKING:
    from src.app import App


class TextAlign(Enum):
    """Text alignment.
    """
    CENTER = 0
    LEFT = 1
    RIGHT = 2

    @classmethod
    def apply(cls, method: Self, text: 'Text'):
        """Apply alignment to the text.
        """
        actions: dict = {
            cls.CENTER: [
                lambda x: x - text.image.get_size()[0] / 2,
                lambda y: y - text.image.get_size()[1] / 2,
            ],
            cls.LEFT: [
                lambda x: x,
                lambda y: y,
            ]
        }
        text.position.x = actions[method][0](text.position.x)
        text.position.y = actions[method][1](text.position.y)


class Text(Sprite):
    """The class responsible for the text.
    """

    def __init__(self, app: 'App', position: Vector2, text: str, font_size: int = 16,
                 color: tuple[int, int, int, int] | tuple[int, int, int] = (255, 255, 255),
                 align: TextAlign = TextAlign.CENTER,
                 max_wight: Optional[int] = None,
                 font_path: str = os.path.join('assets', 'fonts', 'MainFont.ttf'),
                 ):
        """Initialization.

        Args:
            app: The main class of the application.
            position: The position of the sprite on the screen.
            text: Displayed text.
            font_size: Font size.
            color: Font color.
            align: Text align.
            max_wight: The maximum width of the text. If you exceed it, the text will be moved.
            font_path: Font path.
        """
        super().__init__(app, (0, 0), position)
        self.text: str = text
        self.color: tuple[int, int, int, int] | tuple[int, int, int] = color
        self.font_size: int = font_size

        self.align: TextAlign = align
        self.max_wight: Optional[int] = max_wight

        self.font_path: str = font_path

        self.update_view()

        TextAlign.apply(align, self)

    def update_view(self):
        self.image = pg.Surface(self._get_surface_size(), SRCALPHA, 32).convert_alpha()
        for line, text in enumerate(self._get_lines()):
            self.image.blit(
                pg.font.Font(self.font_path, self.font_size).render(text, True, self.color),
                (0, line * self._get_line_height()))

    def _get_lines(self) -> list[str]:
        """Getting lines from text if a width limit is set.

        Returns:
            A list of strings.
        """
        if self.text is None:
            return []
        elif self.max_wight is None:
            return [self.text]

        lines: list[str] = []
        line: str = ''
        for word in self.text.split():
            if pg.font.Font(self.font_path, self.font_size).render(line + ' ' + word, True, (0, 0, 0)).get_size()[
                0] > self.max_wight:
                lines.append(line[:])
                line = ''
            line += ' ' + word

        if line != '':
            lines.append(line)

        return lines

    def _get_line_height(self) -> int:
        """Getting the line height.

        Returns:
            Row height
        """
        return pg.font.Font(self.font_path, self.font_size).render('#', True, (0, 0, 0)).get_size()[1]

    def _get_surface_size(self) -> tuple[int, int]:
        """Getting the image size.

        Returns:
            Getting the image size.
        """
        wight = pg.font.Font(self.font_path, self.font_size).render(self.text, True, self.color).get_size()[0]
        if self.max_wight is not None and self.max_wight < wight:
            wight = self.max_wight

        height: int = self._get_line_height() * len(self._get_lines())

        return wight, height

    async def update(self):
        pass


class InBlockText(Text):
    """Text to insert into other objects.
    """

    def __init__(self, app: 'App', text: str, color: tuple[int, int, int, int] | tuple[int, int, int] = (255, 255, 255),
                 font_size: int = 16, font_path: str = os.path.join('assets', 'fonts', 'MainFont.ttf')):
        """Initialization.

        Args:
            app: The main class of the application.
            text: Displayed text.
            font_size: Font size.
            color: Font color.
            font_path: Font path.
        """
        super().__init__(app, Vector2(0, 0), text, font_size, color, TextAlign.CENTER, None, font_path)

    def correct_position(self, size: tuple[int, int]):
        """Correct the position.
        """
        self.position.x = int(size[0] / 2) - int(self.image.get_size()[0] / 2)
        self.position.y = int(size[1] / 2) - int(self.image.get_size()[1] / 2)

    def update_view(self):
        super().update_view()

    async def update(self):
        await super().update()


class TextSettings(InBlockText):
    """Future text settings.
    """

    def __init__(self, app: 'App', font_size: int = 16,
                 color: tuple[int, int, int, int] | tuple[int, int, int] = (255, 255, 255),
                 font_path: str = os.path.join('assets', 'fonts', 'MainFont.ttf')):
        """Initialization.

        Args:
            app: The main class of the application.
            font_size: Font size.
            color: Font color.
            font_path: Font path.
        """
        super().__init__(app, '', color, font_size, font_path)

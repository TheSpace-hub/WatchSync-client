"""A scene module with an intro.
"""
import os.path
from typing import TYPE_CHECKING, Optional, Coroutine
import pygame as pg
from math import sin
import time

from pygame import Vector2

from src.scene import Scene

from src.sprites import Text, Button, InBlockText, TextAlign, Input, TextSettings

if TYPE_CHECKING:
    from src.app import App


class Intro(Scene):
    """A class with an intro.
    """

    def __init__(self, app: 'App'):
        super().__init__(app)

    async def boot(self):
        self.add_sprite('application_name', Text(self.app, Vector2(10, 10), 'Смотри Синхронно', 32,
                                                 align=TextAlign.LEFT))

        self.add_sprite('server_url', Input(self.app, Vector2(510, 505), (900, 70), TextSettings(self.app),
                                            InBlockText(self.app, 'Адрес сервера', (128, 128, 128)),
                                            default='127.0.0.1:36668'))
        self.add_sprite('watching_the_rocket_button', Button(self.app, Vector2(760, 585), (400, 50),
                                                             InBlockText(self.app, 'Подключиться с серверу')))

    async def update(self):
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            self.app.quit()

    async def enter(self):
        pass

    async def exit(self):
        pass

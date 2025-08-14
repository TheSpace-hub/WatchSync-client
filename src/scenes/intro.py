"""A scene module with an intro.
"""
import os.path
from typing import TYPE_CHECKING, Optional, Coroutine
import pygame as pg
from math import sin
import time

from pygame import Vector2

from src.scene import Scene

from src.sprites import Text, Button, InBlockText, TextAlign, Input, TextSettings, Waiting, CompletionStatus

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
        self.add_sprite('connect_button', Button(self.app, Vector2(760, 585), (400, 50),
                                                 InBlockText(self.app, 'Подключиться с серверу'),
                                                 self.on_connect_button_pressed))

    async def on_connect_button_pressed(self, context: str):
        connect_button: Button = self.get_sprite('connect_button')
        connect_button.disabled = True
        self.add_sprite('connect_waiting', Waiting(self.app, Vector2(760, 645), (400, 30),
                                                   CompletionStatus.WORKING))

    async def update(self):
        pass

    async def enter(self):
        pass

    async def exit(self):
        pass

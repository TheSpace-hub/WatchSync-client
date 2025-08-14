"""A scene module with an intro.
"""
import asyncio
from typing import TYPE_CHECKING, Optional
from asyncio import Task

import ipaddress
import aiohttp
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
        self.taste_connection_task: Optional[Task] = None

    async def boot(self):
        self.add_sprite('application_name', Text(self.app, Vector2(10, 10), 'Смотри Синхронно', 32,
                                                 align=TextAlign.LEFT))

        self.add_sprite('server_url_input', Input(self.app, Vector2(510, 505), (900, 70), TextSettings(self.app),
                                                  InBlockText(self.app, 'Адрес сервера', (128, 128, 128)),
                                                  default='127.0.0.1'))
        self.add_sprite('taste_connection_button', Button(self.app, Vector2(760, 585), (400, 50),
                                                          InBlockText(self.app, 'Подключиться с серверу'),
                                                          self.on_taste_connection_button_pressed))

    async def update(self):
        await self.update_taste_connection_task()

    async def on_taste_connection_button_pressed(self, context: str):
        server_url_input: Input = self.get_sprite('server_url_input')
        connect_button: Button = self.get_sprite('taste_connection_button')

        host = server_url_input.text.text
        if not self.is_valid_ip(host):
            return

        connect_button.disabled = True
        server_url_input.disabled = True

        self.add_sprite('connect_waiting', Waiting(self.app, Vector2(760, 645), (400, 30),
                                                   CompletionStatus.WORKING))

        self.taste_connection_task = asyncio.create_task(self.can_connect(host))

    async def update_taste_connection_task(self):
        """Update taste connection task.
        """
        if self.taste_connection_task and self.taste_connection_task.done():
            waiting: Waiting = self.get_sprite('connect_waiting')
            can_connect: bool = await self.taste_connection_task

            if not can_connect:
                server_url_input: Input = self.get_sprite('server_url_input')
                connect_button: Button = self.get_sprite('taste_connection_button')

                waiting.completion_status = CompletionStatus.ERROR
                connect_button.disabled = False
                server_url_input.disabled = False
                return

            waiting.completion_status = CompletionStatus.SUCCESS
            await self.app.change_scene('Cinema')

    @staticmethod
    async def can_connect(host: str) -> bool:
        """Make a get request.

        Returns:
            Response data.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://{host}:22020/taste') as response:
                return (await response.json())['delicious']

    @staticmethod
    def is_valid_ip(ip_str):
        try:
            ipaddress.ip_address(ip_str)
            return True
        except ValueError:
            return False

    async def enter(self):
        pass

    async def exit(self):
        pass

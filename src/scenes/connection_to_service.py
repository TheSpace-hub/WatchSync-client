"""The stage module with a connection to the service.

This is where the connection to the service takes place https://httpbin.org, which
specifically simulates a delay of 5 seconds.

"""
import asyncio
from asyncio import Task
from typing import TYPE_CHECKING, Optional

import aiohttp
from aiohttp import ContentTypeError, ClientConnectorDNSError, ClientConnectorError
import webbrowser

from pygame import Vector2
import pygame as pg

from src.scene import Scene

from src.sprites import Text, TextAlign, Waiting, CompletionStatus, Input, TextSettings, InBlockText, Button

if TYPE_CHECKING:
    from src.app import App


class ConnectionToService(Scene):
    """A class with a connection to the service.

    Attributes:
        connection_tasks: Tasks responsible for connection.
    """

    def __init__(self, app: 'App'):
        super().__init__(app)
        self.connection_tasks: dict[str, Optional[Task]] = {}

    async def boot(self):
        self.add_sprite('tip', Text(self.app, Vector2(10, 10), 'Press escape to quit', color=(128, 128, 128),
                                    align=TextAlign.LEFT))

        self.add_sprite('delay_address', Text(self.app, Vector2(10, 50), '* Connecting to httpbin.org/delay/5',
                                              align=TextAlign.LEFT))
        self.add_sprite('delay_waiting', Waiting(self.app, Vector2(45, 90), (400, 30), CompletionStatus.WORKING))

        self.add_sprite('error_500_address', Text(self.app, Vector2(10, 150), '* Connecting to httpbin.org/status/500',
                                                  align=TextAlign.LEFT))
        self.add_sprite('error_500_waiting', Waiting(self.app, Vector2(45, 190), (400, 30), CompletionStatus.WORKING))

        self.add_sprite('get_uuid_address', Text(self.app, Vector2(10, 250), '* Connecting to httpbin.org/uuid',
                                                 align=TextAlign.LEFT))
        self.add_sprite('get_uuid_result', Text(self.app, Vector2(45, 330), 'Random UUID: -',
                                                align=TextAlign.LEFT))
        self.add_sprite('get_uuid_waiting', Waiting(self.app, Vector2(45, 290), (400, 30), CompletionStatus.WORKING))

        self.add_sprite('custom_url_input', Input(self.app, Vector2(45, 400), (800, 50), TextSettings(self.app),
                                                  InBlockText(self.app, 'Write url', (128, 128, 128)),
                                                  default='https://httpbin.org/'))
        self.add_sprite('connect_button', Button(self.app, Vector2(855, 400), (150, 50),
                                                 InBlockText(self.app, 'Connect'), self._on_connect_button_pressed))
        self.add_sprite('httpbin_docs_button', Button(self.app, Vector2(1015, 400), (100, 50),
                                                      InBlockText(self.app, 'Docs'),
                                                      self._on_httpbin_docs_button_pressed))
        self.add_sprite('custom_url_waiting', Waiting(self.app, Vector2(45, 460), (400, 30), CompletionStatus.HOLD))

    async def update(self):
        await self.update_tasks()

        if pg.key.get_pressed()[pg.K_ESCAPE]:
            self.app.quit()

    async def enter(self):
        self.connection_tasks['delay_waiting'] = asyncio.create_task(self.fetch_get('https://httpbin.org/delay/5'))
        self.connection_tasks['error_500_waiting'] = asyncio.create_task(
            self.fetch_get('https://httpbin.org/status/500'))
        self.connection_tasks['get_uuid_waiting'] = asyncio.create_task(self.fetch_get('https://httpbin.org/uuid'))

    async def exit(self):
        pass

    async def update_tasks(self):
        """Update all the tasks responsible for the connection.
        """
        completed_keys: list[str] = []
        for key, task in self.connection_tasks.items():
            if task and task.done():
                waiting: Waiting = self.get_sprite(key)
                response: dict = await task
                completed_keys.append(key)

                if response is None:
                    waiting.completion_status = CompletionStatus.ERROR
                    continue

                waiting.completion_status = CompletionStatus.get_status_by_response_status_code(response['status'])

                if key == 'get_uuid_waiting' and response['status'] == 200:
                    get_uuid_result: Text = self.get_sprite('get_uuid_result')
                    get_uuid_result.text = f'Random UUID: {response['body']['uuid']}'
                    get_uuid_result.update_view()

        for key in completed_keys:
            await self.connection_tasks.pop(key)

    @staticmethod
    async def fetch_get(url) -> Optional[dict]:
        """Make a get request.

        Returns:
            Response data.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    try:
                        return {
                            'status': response.status,
                            'headers': response.headers,
                            'body': await response.json()
                        }
                    except ContentTypeError:
                        return {
                            'status': response.status,
                            'headers': response.headers,
                            'body': {}
                        }
        except ClientConnectorDNSError or ClientConnectorError:
            return None

    async def _on_connect_button_pressed(self, context: Optional[str]):
        """The handler for clicking on the button.
        """
        url: Input = self.get_sprite('custom_url_input')
        custom_url_waiting: Waiting = self.get_sprite('custom_url_waiting')

        self.connection_tasks['custom_url_waiting'] = asyncio.create_task(self.fetch_get(url.text.text))
        custom_url_waiting.completion_status = CompletionStatus.WORKING

    async def _on_httpbin_docs_button_pressed(self, context: Optional[str]):
        """The handler for clicking on the button.
        """
        webbrowser.open('https://httpbin.org/')

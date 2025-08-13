"""The main module of the application.

Implements the main application cycle, scenes management (states) and rendering.
"""
import asyncio
import os
import logging
from typing import Any, TypeVar, Type, Optional, Awaitable

from colorlog import ColoredFormatter

import pygame as pg
from pygame import Surface
from pygame.time import Clock

from src.scene import Scene
from src.audio import Audio

# DO NOT DELETE IMPORT. It is necessary that all child classes of Scene are initialized
from src.scenes import *  # pylint: disable=wildcard-import

SceneT = TypeVar('SceneT', bound=Scene)


class App:
    """The main class that implements the main application cycle, scene management (scenes), and rendering.

    Attributes:
        scenes (dict[str, Scenes]): Dictionary of all registered scenes.
        current_scene (Scene | None): Current active status.
        transmitted_data (dict[str, Any]): Data to transfer between scenes.
        screen (Surface): The main surface for rendering.
        clock (Clock): Timer for FPS control.
        omitted_buttons (list[int]): List of omitted keyboard buttons.
        omitted_mouse_buttons (list[int]): List of omitted mouse buttons.
        is_mouse_move (bool): Mouse movement flag.
        running (bool): Application lifecycle operation flag.
        delta_time (float): Time between frames (in seconds).
        lock_mouse (bool): The mouse cursor lock flag.
        mouse_offset (tuple[int, int]): Mouse offset from the last frame.
        _previous_mouse_location (tuple[int, int]): Previous mouse position.
    """

    def __init__(self):
        """Initialization.
        """
        App.configure_logs()
        pg.init()
        pg.font.init()

        self.audio = Audio()

        self.scenes: dict[str, 'Scene'] = {}
        self.current_scene: Optional['Scene'] = None
        self.transmitted_data: dict[str, Any] = {}

        self.screen: Surface = pg.display.set_mode((1920, 1080))
        self.clock: Clock = Clock()

        self.omitted_buttons: list[int] = []
        self.omitted_mouse_buttons: list[int] = []
        self.is_mouse_move: bool = False

        self.running: bool = True
        self.delta_time: float = 0

        self.lock_mouse: bool = False
        self._previous_mouse_location: tuple[int, int] = (0, 0)
        self.mouse_offset: tuple[int, int] = (0, 0)

        pg.display.set_caption('Pygame Application')

    async def loop(self):
        """The start of the application lifecycle.
        """
        while self.running:
            self.omitted_buttons = []
            self.omitted_mouse_buttons = []
            self.is_mouse_move = False
            self.mouse_offset = (0, 0)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    logging.debug('Exit the program by pressing the external exit button.')
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    try:
                        key = ord(event.unicode)
                        logging.debug('Pressing the "%s" key', key)
                        self.omitted_buttons.append(ord(event.unicode))
                    except ValueError:
                        pass
                    except TypeError:
                        pass
                elif event.type == pg.MOUSEBUTTONDOWN:
                    logging.debug('Pressing the mouse button %s', event.button)
                    self.omitted_mouse_buttons.append(event.button)
                if event.type == pg.MOUSEMOTION:
                    self.is_mouse_move = True
                    self.mouse_offset = (pg.mouse.get_pos()[0] - self._previous_mouse_location[0],
                                         pg.mouse.get_pos()[1] - self._previous_mouse_location[1])
                    if self.lock_mouse:
                        pg.mouse.set_pos(self._previous_mouse_location)
                    else:
                        self._previous_mouse_location = pg.mouse.get_pos()
            self.delta_time = self.clock.tick(60) / 1000

            await self.update()

        pg.quit()

    async def update(self):
        """Updating the active scene.
        """
        if self.current_scene:
            await self.current_scene.update()
            tasks: list[Awaitable[None]] = []
            for sprite in list(self.current_scene.sprites.values()):
                tasks.append(sprite.update())
            await asyncio.gather(*tasks)

            self.update_view()

    def update_view(self):
        """Draws objects on the active scene.
        """
        x_factor = pg.display.get_window_size()[0] / 1920
        y_factor = pg.display.get_window_size()[1] / 1080
        self.screen.fill((32, 32, 32))
        for sprite in self.current_scene.sprites.values():
            self.screen.blit(sprite.image,
                             pg.Rect(sprite.position.x * x_factor, sprite.position.y * y_factor, 0, 0))
        pg.display.flip()

    async def init_scenes(self):
        """Initializing scenes.
        """
        logging.debug('Initializing all scenes.')
        tasks: list[Awaitable[None]] = []
        for scene in Scene.__subclasses__():
            tasks.append(asyncio.create_task(self.register_scene(scene)))
        await asyncio.gather(*tasks)

    async def register_scene(self, scene: Type[SceneT]):
        """Registration of a new scene.

        Args:
            scene (Type[SceneT]): Scene class.
        """
        logging.debug('Initializing the scene %s.', scene.__name__)
        self.scenes[str(scene.__name__)] = scene(self)
        await self.scenes[str(scene.__name__)].boot()

    async def change_scene(self, scene: str, transmitted_data: Optional[dict[str, Any]] = None):
        """Switches the scene by the name of the scene class.

        Args:
            scene: The name of the scene class.
            transmitted_data: Data to transfer.
        """
        if transmitted_data is None:
            transmitted_data = {}
        if scene not in self.scenes:
            logging.error('The scene with name %s is not registered.', scene)
            return

        if self.current_scene is not None:
            await self.current_scene.exit()

        self.current_scene = self.scenes[scene]
        self.transmitted_data = transmitted_data
        await self.current_scene.enter()
        self.transmitted_data = {}

    def quit(self):
        """End of the application lifecycle.
        """
        logging.info('Exiting the program.')
        self.running = False

    @staticmethod
    def configure_logs():
        """Configuring logs.
        """
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
        logging.getLogger('werkzeug').disabled = True

        log_format = '[%(asctime)s][%(levelname)s] %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'

        handlers = [
            logging.FileHandler(
                os.path.join('logs', 'server.stderr'),
                encoding='utf-8',
                mode='w'),
            logging.StreamHandler()
        ]

        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            datefmt=date_format,
            handlers=handlers
        )

        root_logger = logging.getLogger()

        console_formatter = ColoredFormatter(
            fmt='%(log_color)s' + log_format + '%(reset)s',
            datefmt=date_format,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )

        for handler in root_logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setFormatter(console_formatter)

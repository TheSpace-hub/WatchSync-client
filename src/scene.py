"""The application's stage module.
"""
import logging
from typing import TYPE_CHECKING, TypeVar, Optional
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from src.app import App
    from src.sprite import Sprite

SpriteT = TypeVar('SpriteT', bound='Sprite')


class Scene(ABC):
    """An abstract base class for application scenes.

    Attributes:
        app (App): The main class of the application.
        sprites (dict[str, Sprite]): A dictionary with the sprite id as its key and the sprite itself as its value.
    """

    def __init__(self, app: 'App'):
        """Initialization

        Args:
            app: The main class of the application.
        """
        self.app: 'App' = app
        self.sprites: dict[str, 'Sprite'] = {}

    def get_sprite(self, uuid: str) -> Optional[SpriteT]:
        """Returns a sprite by its unique identifier.

        Args:
            uuid: The unique identifier of the sprite.

        Returns:
            Sprite or None if the sprite does not exist.
        """
        if uuid in self.sprites:
            return self.sprites[uuid]

        logging.warning('An attempt to get a non-existent sprite "%s".', uuid)
        return None

    def get_sprites(self) -> dict[str, SpriteT]:
        """Returns all sprites of the scene.

        Returns:
            Dictionary of all sprites in {uuid:sprite} format.
        """
        return self.sprites

    def remove_sprite(self, uuid):
        """Удаляет спрайт из сцены.

        Args:
            uuid: Уникальный идентификатор спрайта для удаления
        """
        if uuid in self.sprites:
            del self.sprites[uuid]
        else:
            logging.warning('Attempt to delete a non-existent sprite "%s".', uuid)

    def add_sprite(self, uuid: str, obj: SpriteT) -> SpriteT:
        """Adds a new sprite to the scene.

        Args:
            uuid: The unique identifier of the sprite.
            obj: Object to add.

        Returns:
            Added sprite (same as in the obj parameter).
        """
        self.sprites[uuid] = obj
        return obj

    @abstractmethod
    async def boot(self):
        """It starts when the scene is registered.
        """

    @abstractmethod
    async def update(self):
        """Updating the scene.
        """

    @abstractmethod
    async def enter(self):
        """Called when going to the stage.
        """

    @abstractmethod
    async def exit(self):
        """Called when exiting the scene.
        """

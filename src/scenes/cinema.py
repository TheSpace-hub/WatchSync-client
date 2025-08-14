"""A scene module with a cinema.
"""
from typing import TYPE_CHECKING, Optional
from asyncio import Task

from src.scene import Scene

if TYPE_CHECKING:
    from src.app import App


class Cinema(Scene):
    """A class with a cinema.
    """

    def __init__(self, app: 'App'):
        super().__init__(app)
        self.connection_task: Optional[Task] = None

    async def boot(self):
        pass

    async def update(self):
        pass

    async def enter(self):
        pass

    async def exit(self):
        pass

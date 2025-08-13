"""The main program file.
"""
import asyncio

from src.app import App


async def main():
    """The function starts when the program is started.
    """
    app = App()
    await app.init_scenes()
    await app.change_scene('Intro')
    await app.loop()


if __name__ == '__main__':
    asyncio.run(main())

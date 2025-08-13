"""A module for working with audio.
"""
from typing import Optional
import logging
import pygame as pg
from pygame.mixer import SoundType


class Audio:
    """A class for uploading and playing sounds.
    """

    def __init__(self):
        self.sounds: dict[str, SoundType] = {}

    def load_sound(self, name: str, path: str):
        """Upload an audio file.

        Args:
            name: Sound name.
            path: The path to the audio file
        """
        if name in self.sounds:
            logging.warning("Звук %s уже загружен", name)
            return
        self.sounds[name] = pg.mixer.Sound(path)

    def load_sounds(self, sounds: dict[str, str]):
        """Upload some audio.

        Args:
            A dictionary of sounds, where the key is the name of the sound,and the values are the path to the sound file.
        """
        for name in sounds:
            self.load_sound(name, sounds[name])

    def play(self, name: str, loops: int = 0):
        """Play a sound.

        Args:
            name: Sound name.
            loops: Number of repetitions.
        """
        if name in self.sounds:
            self.sounds[name].play(loops=loops)

    def set_volume(self, name: str, volume: float):
        """Set the sound volume.

        Args:
            name: Sound name.
            volume: Sound volume [0; 1]
        """
        if name in self.sounds:
            self.sounds[name].set_volume(volume)

    def stop(self, name: Optional[str] = None):
        """Stop the sound.

        Args:
            name: Sound name.
        """
        if name is None:
            for sound_name, sound in self.sounds.items():
                sound.stop()
        else:
            if name in self.sounds:
                self.sounds[name].stop()

from typing import Union
from random import choice

import pygame as pg


# Над файлом работала Катя.
class Music:
    def __init__(self, path: Union[str, list], volume: float = 0) -> None:
        self.is_play = None
        self.list_path = path if type(path) == list else None
        self.path = path if type(path) == str else choice(self.list_path)
        self.volume = volume
        self.set_music(self.path)

    def next(self) -> None:
        self.stop()
        ind = self.list_path.index(self.path) + 1
        self.set_music(self.list_path[ind % len(self.list_path)])
        self.play()

    def get_text(self) -> str:
        n = max([i for i, char in enumerate(self.path) if char == '/']) + 1
        k = max([i for i, char in enumerate(self.path) if char == '.'])
        return self.path[n:k]

    def previous(self) -> None:
        self.stop()
        ind = self.list_path.index(self.path) + len(self.list_path) - 1
        self.set_music(self.list_path[ind % len(self.list_path)])
        self.play()

    def set_music(self, path: str) -> None:
        self.path = path
        pg.mixer.music.load(path)
        pg.mixer.music.set_volume(self.volume)

    def update(self, volume: float) -> None:
        self.volume = volume
        pg.mixer.music.set_volume(self.volume)

    def play(self) -> None:
        if self.is_play is None:
            pg.mixer.music.play(-1)
        elif not self.is_play:
            pg.mixer.music.unpause()
        self.is_play = True

    def stop(self) -> None:
        pg.mixer.music.stop()
        self.is_play = None

    def pause(self) -> None:
        self.is_play = False
        pg.mixer.music.pause()

    def pause_and_play(self) -> None:
        if self.is_play:
            self.pause()
        else:
            self.play()

    def get_state(self) -> int:
        return 1 if self.is_play else 0


class Sound:
    def __init__(self, volumes: dict) -> None:
        self.volumes = volumes
        self.paths_sounds = set()

    def update(self, name: str, volume: float) -> None:
        pass

    def play(self) -> None:
        for path in self.paths_sounds:
            sound = pg.mixer.Sound(path)
            for name in self.volumes.keys():
                if name in path:
                    sound.set_volume(self.volumes[name].value)
                    break
            sound.play()
        self.paths_sounds = set()

    def add(self, sound) -> None:
        self.paths_sounds.add(sound)

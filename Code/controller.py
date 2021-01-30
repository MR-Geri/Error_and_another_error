from Code.settings import *
from Code.edit_permission import Permission
from Code.slider import Numbers
from Code.sound import Music, Sound
from Code.window import MenuWindow, SettingsWindow, GameWindow
import json


# Над файлом работали оба.
class Controller:
    def __init__(self) -> None:
        with open(SAVE + 'settings.json', 'r') as file:
            data = json.load(file)
            display_size = tuple(data['display_size'])
        self.icon = pg.image.load('error.png')
        self.volume = Numbers(0, 1, 0.01, round(1 / 16, 3))
        self.volume_sound = {
            'crashes': Numbers(0, 1, 0.01, round(1 / 16, 3)),
            'moves': Numbers(0, 1, 0.01, round(1 / 16, 3)),
            'charge': Numbers(0, 1, 0.01, round(1 / 16, 3)),
            'mine': Numbers(0, 1, 0.01, round(1 / 16, 3))
        }
        self.music = Music(path=ALL_BACKGROUND_MUSIC, volume=self.volume.value)
        self.sound = Sound(self.volume_sound)
        self.permission = Permission(active=display_size)
        if FULL_SCREEN:
            self.display = pg.display.set_mode(self.permission.active, pg.FULLSCREEN)
        else:
            self.display = pg.display.set_mode(self.permission.active)
        pg.display.set_caption(MENU_TITLE)
        pg.display.set_icon(self.icon)
        #
        self.game = GameWindow(self, display_size, self.display)
        self.menu = MenuWindow(self, display_size, self.display)
        self.settings = SettingsWindow(self, display_size, self.display)
        #
        self.windows = {'menu': self.menu, 'settings': self.settings, 'game': self.game}

    def new_game(self) -> None:
        del self.game
        self.game = GameWindow(self, self.permission.active, self.display)
        self.windows['game'] = self.game

    def init(self) -> None:
        with open(SAVE + 'settings.json', 'r') as read:
            data = json.load(read)
            data['display_size'] = list(self.permission.active)
            with open(SAVE + 'settings.json', 'w') as file:
                json.dump(data, file)
        if FULL_SCREEN:
            self.display = pg.display.set_mode(self.permission.active, pg.FULLSCREEN)
        else:
            self.display = pg.display.set_mode(self.permission.active)
        pg.display.set_icon(self.icon)
        del self.menu
        del self.settings
        del self.game
        del self.windows
        self.menu = MenuWindow(self, self.permission.active, self.display)
        self.settings = SettingsWindow(self, self.permission.active, self.display)
        self.game = GameWindow(self, self.permission.active, self.display)
        #
        self.windows = {'menu': self.menu, 'settings': self.settings, 'game': self.game}

    def action_window(self, window_act: str) -> None:
        for window in self.windows.keys():
            if self.windows[window].is_run:
                self.windows[window].join()
                self.windows[window_act].run(last=window)

    def all_off(self) -> None:
        for window in self.windows.keys():
            self.windows[window].join()

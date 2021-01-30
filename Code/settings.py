from typing import Union, Tuple
from os import walk
import pygame as pg
from random import randint, sample, choice


# Настройки окна
WIN_WIDTH, WIN_HEIGHT = 1280, 720
FULL_SCREEN = False
MENU_TITLE = 'Error and another error =/'
FPS = 60
UPDATE_CHANGE_TIME = 1440
CLOCK = pg.time.Clock()
# Цвета
COLOR_BACKGROUND = '#313335'
COLOR_CELL = '#013a33'
COLOR_SLIDER_USE = '#25B2B9'
COLOR_SLIDER_NO_USE = '#D5F0F8'
COLOR_SLIDER_CIRCLE = 'white'
# Камера
MAX_SCALE = 3
CAMERA_K_SPEED_X, CAMERA_K_SPEED_Y = 5, 5
# Ячейки
SECTOR_Y_NUMBER = 50  # Размер сектора
SECTOR_X_NUMBER = 50  # Размер сектора
#
INFO_PANEL_K = 5
# Path
PT_MONO = 'Data/Font/PT Mono.ttf'
MS_MINCHO = 'Data/Font/MS Mincho.ttf'

MENU_BACKGROUND = 'Data/Images/game.jpg'

PATH_CRASHES = 'Data/Sounds/crashes/'
PATH_MOVES = 'Data/Sounds/moves/'
PATH_CHARGE = 'Data/Sounds/charge/'
PATH_MINES = 'Data/Sounds/mines/'
ALL_BACKGROUND_MUSIC = [[root + i for i in files] for root, _, files in walk('Data/Sounds/background_music/')][0]

PLAYER_CODE = 'Game_code/'
SAVE = 'Data/Save/'
# Типизация
COLOR = Union[Tuple[int, int, int], str]
from Code.texts import Text, TextMaxSize, TextMaxSizeCenter, TextCenter
from Code.sector_objects.generates_electrical import RadioisotopeGenerator
STR_TO_OBJECT = {'RadioisotopeGenerator': RadioisotopeGenerator}
ALL_TEXT = Union[Text, TextMaxSize, TextMaxSizeCenter, TextCenter]
from Code.running_line import RunningLineMaxSizeCenter
ALL_RUNNING_LINE = Union[RunningLineMaxSizeCenter]
from Code.Map.cell import (Plain, Swamp, Mountain, Desert,
                           IronOre, GoldOre, CooperOre, TinOre, SiliconOre, PlatinumOre, AluminiumOre)
STR_TO_OBJECT['Plain'] = Plain
STR_TO_OBJECT['Swamp'] = Swamp
STR_TO_OBJECT['Mountain'] = Mountain
STR_TO_OBJECT['Desert'] = Desert

STR_TO_OBJECT['IronOre'] = IronOre
STR_TO_OBJECT['GoldOre'] = GoldOre
STR_TO_OBJECT['CooperOre'] = CooperOre
STR_TO_OBJECT['TinOre'] = TinOre
STR_TO_OBJECT['SiliconOre'] = SiliconOre
STR_TO_OBJECT['PlatinumOre'] = PlatinumOre
STR_TO_OBJECT['AluminiumOre'] = AluminiumOre
ALL_CELL = Union[Plain, Swamp, Mountain, IronOre, AluminiumOre, GoldOre, CooperOre, TinOre, SiliconOre, PlatinumOre]
STR_ORES = ['IronOre', 'AluminiumOre', 'GoldOre', 'CooperOre', 'TinOre', 'SiliconOre', 'PlatinumOre']
from Code.sector_objects.robots import MK0, MK1, MK2, MK3
STR_TO_OBJECT['MK0'] = MK0
STR_TO_OBJECT['MK1'] = MK1
STR_TO_OBJECT['MK2'] = MK2
STR_TO_OBJECT['MK3'] = MK3
ALL_ROBOT = Union[MK0, MK1, MK2, MK3]
from Code.sector_objects.bases import Base
from Code.sector_objects.foundry import Foundry
STR_TO_OBJECT['Base'] = Base
STR_TO_OBJECT['Foundry'] = Foundry
#
from Code.buttons import Button, ButtonTwoStates, ChoiceButton
BUTTONS = [Button, ButtonTwoStates, ChoiceButton]

# Биомы
MAX_SIZE_MOUNTAIN = (10, 10)
MAX_QUANTITY_MOUNTAIN = 7
MIN_QUANTITY_MOUNTAIN_CELL = 7

MAX_SIZE_SWAMP = (20, 20)
MAX_QUANTITY_SWAMP = 5
MIN_QUANTITY_SWAMP_CELL = 8

MAX_SIZE_DESERT = (25, 25)
MAX_QUANTITY_DESERT = 5
MIN_QUANTITY_DESERT_CELL = 10
#
MAX_SIZE_IRON = (4, 4)
MAX_QUANTITY_IRON = 3
MIN_QUANTITY_IRON_CELL = 5

MAX_SIZE_ALUMINIUM = (4, 4)
MAX_QUANTITY_ALUMINIUM = 4
MIN_QUANTITY_ALUMINIUM_CELL = 6

MAX_SIZE_GOLD = (2, 2)
MAX_QUANTITY_GOLD = 2
MIN_QUANTITY_GOLD_CELL = 3

MAX_SIZE_COOPER = (5, 5)
MAX_QUANTITY_COOPER = 4
MIN_QUANTITY_COOPER_CELL = 6

MAX_SIZE_TIN = (4, 4)
MAX_QUANTITY_TIN = 3
MIN_QUANTITY_TIN_CELL = 5

MAX_SIZE_SILICON = (3, 3)
MAX_QUANTITY_SILICON = 1
MIN_QUANTITY_SILICON_CELL = 4

MAX_SIZE_PLATINUM = (2, 2)
MAX_QUANTITY_PLATINUM = 1
MIN_QUANTITY_PLATINUM_CELL = 1
#
SELL_BLOCKED = [Mountain, IronOre, AluminiumOre, GoldOre, CooperOre, TinOre, SiliconOre, PlatinumOre]
#
ROBOTS = [MK0, MK1, MK2]
BASES = [Base, IronOre, AluminiumOre, GoldOre, CooperOre, TinOre, SiliconOre, PlatinumOre]
FOUNDRIES = [Foundry]
#

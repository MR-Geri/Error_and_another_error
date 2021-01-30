from Code.inventory import InventoryRobot
from Code.settings import *
from Code.utils import Path, PermissionsRobot
from Code.dialogs import DialogInfo, DialogFile, DialogState
from Code.info_panel import RightPanel, LeftPanel


# Над файлом работал я.
class Robot:
    def __init__(self, pos: Tuple[int, int], size_cell: int,
                 dialog_info: DialogInfo, dialog_file: DialogFile, dialog_state: DialogState, right_panel: RightPanel,
                 left_panel: LeftPanel) -> None:
        self.pos = list(pos)
        self.size_cell = size_cell
        self.right_panel = right_panel
        self.left_panel = left_panel
        self.dialog_info = dialog_info
        self.dialog_file = dialog_file
        self.dialog_state = dialog_state
        self.unique_name = str(randint(1000000, 9999999))
        # Функции пользователя
        self.move = lambda *args, **kwargs: None
        self.mine = lambda *args, **kwargs: None
        self.item_transfer = lambda *args, **kwargs: None
        # Состояния
        self.permissions = PermissionsRobot()
        self.path_user_code = Path('')
        # Заменяются версией робота
        self.name = 'Робот'
        self.energy = 0
        self.energy_max = 0
        self.energy_create = 0
        self.dmg = 0
        self.hp = 0
        self.hp_max = 0
        self.distance_move = 0
        self.sell_block = ['Mountain'] + STR_ORES
        self.inventory_max = 0
        self.distance_resource = 0
        self.inventory = InventoryRobot(*self.right_panel.inventory_settings, max_items=self.inventory_max)
        # Заменяются версией робота
        self.sound_crash = PATH_CRASHES + 'MK0.wav'
        self.sound_move = PATH_MOVES + 'MK0.wav'
        self.sound_mine = PATH_MINES + 'MK0.mp3'
        #
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        #
        self.render()

    def get_state(self) -> dict:
        data = {
            'name': self.__class__.__name__, 'unique_name': self.unique_name,
            'pos': tuple(self.pos), 'x': self.pos[0], 'y': self.pos[1],
            'hp': self.hp,
            'energy': self.energy, 'energy_max': self.energy_max,
            'damage': self.dmg, 'dmg': self.dmg,
            'sell_block': self.sell_block, 'distance_move': self.distance_move, 'inventory_max': self.inventory_max,
            'distance_resource': self.distance_resource, 'inventory': self.inventory.resources
        }
        for k, v in data.items():
            data[k] = type(v)(v)
        data['permissions'] = self.permissions
        return data

    def pos_update(self, pos: Tuple[int, int]) -> None:
        # НЕ ВЛИЯЕТ пользователь
        self.pos = list(pos)
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        if self.right_panel.info_update == self.info:
            self.info()

    def energy_receiving(self, energy: int) -> None:
        # ВЛИЯЕТ пользователь
        if self.permissions.can_charging:
            self.energy = min(energy + self.energy, self.energy_max)
            if self.right_panel.info_update == self.info:
                self.info()

    def energy_decrease(self, energy: int) -> None:
        # НЕ ВЛИЯЕТ пользователь
        self.energy -= energy
        if self.right_panel.info_update == self.info:
            self.info()

    def move_core(self, board, entities) -> Union[None, Tuple[int, int]]:
        # ВЛИЯЕТ пользователь
        if self.permissions.can_move:
            return self.move(self.get_state(), board, entities)
        return None

    def mine_core(self, board, entities) -> Union[None, Tuple[int, int]]:
        # ВЛИЯЕТ пользователь
        if self.permissions.can_mine:
            return self.mine(self.get_state(), board, entities)
        return None

    def item_transfer_core(self, board, entities) -> Union[None, tuple]:
        # ВЛИЯЕТ пользователь
        if self.permissions.can_item_transfer:
            return self.item_transfer(self.get_state(), board, entities)
        return None

    def info(self) -> None:
        self.right_panel.info_update = self.info
        energy = f'Энергия > {self.energy}'
        hp = f'Прочность > {self.hp}'
        texts = [self.name, 'Уникальное имя', self.unique_name, energy, hp]
        self.right_panel.update_text(texts)

    def save(self) -> dict:
        state = {
            'pos': self.pos, 'unique_name': self.unique_name,
            'path_user_code': self.path_user_code.text, 'name': self.__class__.__name__, 'energy': self.energy,
            'energy_max': self.energy_max, 'dmg': self.dmg, 'hp': self.hp, 'hp_max': self.hp_max,
            'distance_move': self.distance_move, 'permissions': self.permissions.get_state(),
            'distance_resource': self.distance_resource, 'inventory': self.inventory.resources
        }
        return state

    def load(self, state: dict):
        self.pos = state['pos']
        self.unique_name = state['unique_name']
        self.path_user_code = Path(state['path_user_code'])
        self.energy = state['energy']
        self.energy_max = state['energy_max']
        self.hp = state['hp']
        self.hp_max = state['hp_max']
        self.dmg = state['dmg']
        self.distance_move = state['distance_move']
        self.distance_resource = state['distance_resource']
        self.inventory.set_resources(state['inventory'])
        #
        self.permissions = PermissionsRobot(state['permissions'])

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        radius = int(self.size_cell / 2)
        pg.draw.circle(self.surface, pg.Color(255, 255, 255), (radius, radius), radius)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def scale(self, size_cell: int) -> None:
        self.size_cell = size_cell
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.render()

    def func_file(self) -> None:
        self.dialog_file.show(self.path_user_code)

    def func_del_file(self) -> None:
        self.path_user_code.set_text('')
        self.move = lambda *args, **kwargs: None
        self.mine = lambda *args, **kwargs: None
        self.item_transfer = lambda *args, **kwargs: None
        self.left_panel.button_del_file.func = None

    def func_info(self) -> None:
        self.dialog_state.show([
            f'Максимально энергии > {self.energy_max}', f'Дистанция перемещения > {self.distance_move}',
            f'Максимально прочности > {self.hp_max}', f'Наносимый урон > {self.dmg}',
            f'Размер инвентаря > {self.inventory_max}', f'Дистанция передачи предметов > {self.distance_resource}'
        ])


class MK0(Robot):
    def __init__(self, pos: Tuple[int, int], size_cell: int,
                 dialog_info: DialogInfo, dialog_file: DialogFile, dialog_state: DialogState,
                 right_panel: RightPanel, left_panel: LeftPanel) -> None:
        super().__init__(pos, size_cell, dialog_info, dialog_file, dialog_state, right_panel, left_panel)
        self.name = 'Робот MK0'
        self.energy = 50
        self.energy_max = 200
        self.energy_create = 100
        self.resource_create = []
        self.dmg = 0
        self.hp = 100
        self.hp_max = 100
        self.distance_move = 1
        self.sell_block = ['Mountain'] + STR_ORES
        #
        self.inventory_max = 50
        self.distance_resource = 1
        self.inventory = InventoryRobot(*self.right_panel.inventory_settings, max_items=self.inventory_max)

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        radius = int(self.size_cell / 2)
        pg.draw.circle(self.surface, pg.Color(0, 0, 0), (radius, radius), radius)


class MK1(Robot):
    def __init__(self, pos: Tuple[int, int], size_cell: int,
                 dialog_info: DialogInfo, dialog_file: DialogFile, dialog_state: DialogState,
                 right_panel: RightPanel, left_panel: LeftPanel) -> None:
        super().__init__(pos, size_cell, dialog_info, dialog_file, dialog_state, right_panel, left_panel)
        self.name = 'Робот MK1'
        self.energy = 100
        self.energy_max = 400
        self.energy_create = 150
        self.resource_create = []
        self.dmg = 0
        self.hp = 130
        self.hp_max = 130
        self.distance_move = 1
        self.sell_block = ['Mountain'] + STR_ORES
        #
        self.inventory_max = 150
        self.distance_resource = 1
        self.inventory = InventoryRobot(*self.right_panel.inventory_settings, max_items=self.inventory_max)

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        radius = int(self.size_cell / 2)
        pg.draw.circle(self.surface, pg.Color(255, 0, 0), (radius, radius), radius)


class MK2(Robot):
    def __init__(self, pos: Tuple[int, int], size_cell: int,
                 dialog_info: DialogInfo, dialog_file: DialogFile, dialog_state: DialogState,
                 right_panel: RightPanel, left_panel: LeftPanel) -> None:
        super().__init__(pos, size_cell, dialog_info, dialog_file, dialog_state, right_panel, left_panel)
        self.name = 'Робот MK2'
        self.energy = 200
        self.energy_max = 550
        self.energy_create = 200
        self.resource_create = [('Медь', 'продукт', 150), ('Олово', 'продукт', 50), ('Железо', 'продукт', 80)]
        self.dmg = 0
        self.hp = 100
        self.hp_max = 100
        self.distance_move = 2
        self.sell_block = ['Mountain'] + STR_ORES
        #
        self.inventory_max = 300
        self.distance_resource = 1
        self.inventory = InventoryRobot(*self.right_panel.inventory_settings, max_items=self.inventory_max)

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        radius = int(self.size_cell / 2)
        pg.draw.circle(self.surface, pg.Color(255, 255, 0), (radius, radius), radius)


class MK3(Robot):
    def __init__(self, pos: Tuple[int, int], size_cell: int,
                 dialog_info: DialogInfo, dialog_file: DialogFile, dialog_state: DialogState,
                 right_panel: RightPanel, left_panel: LeftPanel) -> None:
        super().__init__(pos, size_cell, dialog_info, dialog_file, dialog_state, right_panel, left_panel)
        self.name = 'Робот MK3'
        self.energy = 200
        self.energy_max = 600
        self.energy_create = 200
        self.resource_create = [('Медь', 'продукт', 100), ('Олово', 'продукт', 50), ('Железо', 'продукт', 180),
                                ('Платина', 'продукт', 15)]
        self.dmg = 0
        self.hp = 200
        self.hp_max = 200
        self.distance_move = 3
        self.sell_block = ['Mountain'] + STR_ORES
        #
        self.inventory_max = 400
        self.distance_resource = 2
        self.inventory = InventoryRobot(*self.right_panel.inventory_settings, max_items=self.inventory_max)

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        radius = int(self.size_cell / 2)
        pg.draw.circle(self.surface, pg.Color(255, 169, 0), (radius, radius), radius)

from Code.settings import *
from Code.inventory import Inventory
from Code.utils import Path, PermissionsFoundry
from Code.dialogs import DialogInfo, DialogFile, DialogState
from Code.info_panel import RightPanel, LeftPanel


# Над файлом работал я.
class Foundry:
    def __init__(self, pos: Tuple[int, int], size_cell: int, dialog_info: DialogInfo, dialog_file: DialogFile,
                 dialog_state: DialogState, right_panel: RightPanel, left_panel: LeftPanel) -> None:
        self.pos = list(pos)
        self.size_cell = size_cell
        self.dialog_info = dialog_info
        self.dialog_file = dialog_file
        self.dialog_state = dialog_state
        self.right_panel = right_panel
        self.left_panel = left_panel
        # Функции пользователя
        self.item_transfer = lambda *args, **kwargs: None
        # Состояния
        self.permissions = PermissionsFoundry()
        # Характеристики
        self.path_user_code = Path('')
        self.name = 'Плавильня'
        self.energy = 0
        self.energy_max = 8000
        self.hp = 1000
        self.hp_max = 1000
        #
        self.sound_charge = PATH_CHARGE + 'MK0.wav'
        #
        self.distance_resource = 5
        self.inventory = Inventory(*self.right_panel.inventory_settings)
        #
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        #
        self.render()

    def get_state(self) -> dict:
        data = {
            'name': self.__class__.__name__, 'pos': tuple(self.pos), 'x': self.pos[0], 'y': self.pos[1],
            'hp': self.hp, 'hp_max': self.hp_max,
            'energy': self.energy, 'energy_max': self.energy_max,
            'distance_resource': self.distance_resource, 'inventory': self.inventory.resources
        }
        for k, v in data.items():
            data[k] = type(v)(v)
        data['permissions'] = self.permissions
        return data

    def render(self) -> None:
        self.surface = pg.Surface((self.size_cell, self.size_cell), pg.SRCALPHA)
        self.surface.fill('#2B21BB')
        s3 = int(self.size_cell / 3)
        pg.draw.rect(self.surface, pg.Color('#4D6E75'), (s3, 0, self.size_cell - 2*s3, self.size_cell))
        pg.draw.rect(self.surface, pg.Color('#4D6E75'), (0, s3, self.size_cell, self.size_cell - 2*s3))

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def info(self) -> None:
        self.right_panel.info_update = self.info
        energy = f'Энергия > {self.energy}'
        hp = f'Прочность > {self.hp}'
        texts = [self.name, energy, hp]
        self.right_panel.update_text(texts)

    def save(self) -> dict:
        state = {
            'pos': self.pos,
            'path_user_code': self.path_user_code.text, 'name': self.__class__.__name__,
            'energy': self.energy, 'energy_max': self.energy_max, 'hp': self.hp, 'hp_max': self.hp_max,
            'permissions': self.permissions.get_state(), 'inventory': self.inventory.resources,
            'distance_resource': self.distance_resource
        }
        return state

    def load(self, state: dict):
        self.pos = state['pos']
        self.path_user_code = Path(state['path_user_code'])
        self.energy = state['energy']
        self.energy_max = state['energy_max']
        self.hp = state['hp']
        self.hp_max = state['hp_max']
        self.distance_resource = state['distance_resource']
        self.inventory.set_resources(state['inventory'])
        self.permissions = PermissionsFoundry(state['permissions'])

    def scale(self, size_cell: int) -> None:
        self.size_cell = size_cell
        self.rect = pg.Rect(self.pos[0] * self.size_cell, self.pos[1] * self.size_cell, self.size_cell, self.size_cell)
        self.render()

    def process(self) -> None:
        for resource in self.inventory.resources:
            quantity = self.inventory.resources[resource]['сырьё']
            if 0 < self.energy:
                quantity = self.energy if quantity > self.energy else quantity
                self.energy_decrease(quantity)
                self.inventory.update(resource, False, -quantity)
                self.inventory.update(resource, True, quantity)

    def energy_decrease(self, energy: int) -> None:
        # НЕ ВЛИЯЕТ пользователь
        self.energy -= energy
        if self.right_panel.info_update == self.info:
            self.info()

    def energy_receiving(self, energy: int) -> None:
        # ВЛИЯЕТ пользователь
        if self.permissions.can_charging:
            self.energy = min(energy + self.energy, self.energy_max)
            if self.right_panel.info_update == self.info:
                self.info()

    def item_transfer_core(self, board, entities) -> Union[None, tuple]:
        # ВЛИЯЕТ пользователь
        if self.permissions.can_item_transfer:
            return self.item_transfer(self.get_state(), board, entities)
        return None

    def func_file(self) -> None:
        self.dialog_file.show(self.path_user_code)  # Установка файла

    def func_del_file(self) -> None:
        self.path_user_code.set_text('')
        self.left_panel.button_del_file.func = None

    def func_info(self) -> None:
        self.dialog_state.show([
            f'Максимально энергии > {self.energy_max}', f'Максимальная прочность > {self.hp_max}',
            f'Дальность передачи предметов > {self.distance_resource}'
        ])

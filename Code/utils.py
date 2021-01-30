from Code.settings import *
import math


# Над файлом работал я.
class InterfaceError(Exception):
    pass


class Interface:
    def __init__(self, pos: Tuple[int, int], max_width: int = None, max_height: int = None,
                 indent: Tuple[int, int] = None, size: Tuple[int, int] = None):
        self.start_pos = pos
        self.pos = list(pos)
        self.x, self.y = self.pos
        self.max_width = max_width
        self.max_height = max_height
        self.indent = indent
        self.size = size
        self.width, self.height = self.size

    def move(self, width: int = None, height: int = None, is_indent: Tuple[bool, bool] = (True, True)):
        width = self.size[0] if width is None else width
        height = self.size[1] if height is None else height
        #
        if not self.max_width or self.pos[0] + width <= self.max_width + self.start_pos[0]:
            self.pos[0] += width
            self.pos[0] += self.indent[0] if is_indent[0] else 0
        else:
            raise InterfaceError("Выход за границы окна.")
        #
        if not self.max_height or self.pos[1] + height <= self.max_height + self.start_pos[1]:
            self.pos[1] += height
            self.pos[1] += self.indent[1] if is_indent[1] else 0
        else:
            raise InterfaceError("Выход за границы окна.")
        #
        self.x, self.y = self.pos


class Path:
    def __init__(self, text: str) -> None:
        self.text = text
        self.last_code = None

    def set_text(self, text: str) -> None:
        self.text = text
        self.last_code = None

    def module(self) -> Union[str, None]:
        return self.text.split(r'Error_and_another_error\ '[:-1])[1].split('.py')[0].replace(r'\ '[0], '.')

    def code(self) -> Union[None, list]:
        with open(self.text) as commands:
            try:
                t = commands.read().split('\n\n\n')
                data = {i.split("def ")[1].split("(")[0]: i for i in t if 'def' in i}
                if data != self.last_code:
                    self.last_code = data
                else:
                    return None
            except Exception as e:
                print(e)
                return None
        return list(self.last_code.keys())


class PermissionsRobot:
    def __init__(self, states: dict = None) -> None:
        if states is None:
            states = {'can_move': True, 'can_charging': True, 'can_mine': True, 'can_item_transfer': True}
        self.can_move = states['can_move']
        self.can_charging = states['can_charging']
        self.can_mine = states['can_mine']
        self.can_item_transfer = states['can_item_transfer']

    def set_move(self, flag: bool) -> None:
        self.can_move = flag

    def set_charging(self, flag: bool) -> None:
        self.can_charging = flag

    def set_mine(self, flag: bool) -> None:
        self.can_mine = flag

    def set_item_transfer(self, flag: bool) -> None:
        self.can_item_transfer = flag

    def get_state(self) -> dict:
        return {'can_move': self.can_move, 'can_charging': self.can_charging, 'can_mine': self.can_mine,
                'can_item_transfer': self.can_item_transfer}


class PermissionsBase:
    def __init__(self, states: dict = None) -> None:
        if states is None:
            states = {'can_charging': True, 'can_generate': True, 'can_item_transfer': True}
        self.can_charging = states['can_charging']
        self.can_generate = states['can_generate']
        self.can_item_transfer = states['can_item_transfer']

    def set_charging(self, flag: bool) -> None:
        self.can_charging = flag

    def set_generate(self, flag: bool) -> None:
        self.can_generate = flag

    def set_item_transfer(self, flag: bool) -> None:
        self.can_item_transfer = flag

    def get_state(self) -> dict:
        return {'can_charging': self.can_charging, 'can_generate': self.can_generate,
                'can_item_transfer': self.can_item_transfer}


class PermissionsFoundry:
    def __init__(self, states: dict = None) -> None:
        if states is None:
            states = {'can_melt': True, 'can_item_transfer': True, 'can_charging': True}
        self.can_melt = states['can_melt']
        self.can_item_transfer = states['can_item_transfer']
        self.can_charging = states['can_charging']

    def set_melt(self, flag: bool) -> None:
        self.can_melt = flag

    def set_item_transfer(self, flag: bool) -> None:
        self.can_item_transfer = flag

    def set_charging(self, flag: bool) -> None:
        self.can_charging = flag

    def get_state(self) -> dict:
        return {'can_melt': self.can_melt, 'can_item_transfer': self.can_item_transfer,
                'can_charging': self.can_charging}


class Dial:
    def __init__(self, pos: Tuple[int, int], side: int, max_value: int, circle_color: COLOR, line_color: COLOR) -> None:
        self.rect = pg.Rect(*pos, side, side)
        self.surface = pg.Surface((side, side), pg.SRCALPHA)
        self.max_value = max_value
        self.value = 0
        self.circle_color = circle_color
        self.line_color = line_color

    @staticmethod
    def get_pos(angle: int, radius: int) -> Tuple[int, int]:
        x = int(radius + radius * math.cos(math.radians(angle) - math.pi / 2))
        y = int(radius + radius * math.sin(math.radians(angle) - math.pi / 2))
        return x, y

    def render(self, value: int) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        radius = self.rect.height // 2
        pg.draw.circle(self.surface, pg.Color(self.circle_color), (radius, radius), radius, max(1, int(radius / 7)))
        pos = self.get_pos(int(value / self.max_value * 360), radius)
        pg.draw.line(self.surface, pg.Color(self.line_color), (radius, radius), pos, max(1, int(radius / 7)))

    def draw(self, surface: pg.Surface, value: int) -> None:
        if value != self.value:
            self.render(value)
            self.value = value
        surface.blit(self.surface, self.rect)

from Code.settings import *
from Code.texts import max_size_list_text, Texts
from Code.utils import Interface


# Над файлом работали оба.
class Inventory:
    def __init__(self, pos: Tuple[int, int], width: int, height: int) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((width, height))
        self.w80, self.w10 = int(self.rect.width * 0.5), int(self.rect.width * 0.25)
        self.resources = {
            'Железо': {'продукт': 0, 'сырьё': 0},
            'Алюминий': {'продукт': 0, 'сырьё': 0},
            'Золото': {'продукт': 0, 'сырьё': 0},
            'Медь': {'продукт': 0, 'сырьё': 0},
            'Олово': {'продукт': 0, 'сырьё': 0},
            'Кремний': {'продукт': 0, 'сырьё': 0},
            'Платина': {'продукт': 0, 'сырьё': 0},
        }
        self.texts = {
            'Железо': {'продукт': None, 'сырьё': None},
            'Алюминий': {'продукт': None, 'сырьё': None},
            'Золото': {'продукт': None, 'сырьё': None},
            'Медь': {'продукт': None, 'сырьё': None},
            'Олово': {'продукт': None, 'сырьё': None},
            'Кремний': {'продукт': None, 'сырьё': None},
            'Платина': {'продукт': None, 'сырьё': None}
        }
        self.if_update: bool = False
        self.render_init()

    def is_it_empty(self) -> bool:
        if sum([sum(i.values()) for i in self.resources.values()]) != 0:
            return True
        return False

    def check(self, resources: list) -> bool:
        for resource in resources:
            name, condition, quantity = resource
            if self.resources[name][condition] < quantity:
                return False
        return True

    def update(self, resource: str, condition: Union[str, bool] = False, quantity: int = 0) -> None:
        if type(condition) == bool:
            condition = 'продукт' if condition else 'сырьё'
        if 100000 >= self.resources[resource][condition] + quantity >= 0:
            self.resources[resource][condition] += quantity
            self.texts[resource][condition].set_text(f'{self.resources[resource][condition]}')
            self.render()

    def render_init(self) -> None:
        self.surface.fill(COLOR_BACKGROUND)
        interface = Interface((0, 0), max_width=self.rect.width, max_height=self.rect.height,
                              indent=(0, self.rect.height // 54), size=(self.rect.width, self.rect.height // 9))
        size = max_size_list_text(['Продукт', 'Сырьё'], self.w10, interface.height, font_type=PT_MONO)
        #
        text = TextMaxSizeCenter(text=f'Ресурс', pos=interface.pos, width=self.w80, height=interface.height,
                                 font_type=PT_MONO)
        text.draw(self.surface)
        text = TextCenter(text=f'Продукт', pos=(interface.pos[0] + self.w80, interface.pos[1]),
                          width=self.w10, height=interface.height, font_size=size, font_type=PT_MONO)
        text.draw(self.surface)
        text = TextCenter(text=f'Сырьё', pos=(interface.pos[0] + self.w80 + self.w10, interface.pos[1]),
                          width=self.w10, height=interface.height, font_size=size, font_type=PT_MONO)
        text.draw(self.surface)
        interface.move(0)
        for element in self.resources.keys():
            text = TextMaxSizeCenter(text=element, pos=interface.pos, width=self.w80, height=interface.height,
                                     font_type=PT_MONO)
            text.draw(self.surface)
            text = TextMaxSizeCenter(text=str(self.resources[element]['продукт']),
                                     pos=(interface.pos[0] + self.w80, interface.pos[1]),
                                     width=self.w10, height=interface.height, font_type=PT_MONO)
            self.texts[element]['продукт'] = text
            text.draw(self.surface)
            text = TextMaxSizeCenter(text=str(self.resources[element]['сырьё']),
                                     pos=(interface.pos[0] + self.w80 + self.w10, interface.pos[1]),
                                     width=self.w10, height=interface.height, font_type=PT_MONO)
            self.texts[element]['сырьё'] = text
            text.draw(self.surface)
            interface.move(0)
        self.render()

    def render(self) -> None:
        if self.resources:
            pos = (self.w80, self.rect.height // 54 + self.rect.height // 9)
            pg.draw.rect(
                self.surface, pg.Color(COLOR_BACKGROUND),
                (pos[0], pos[1], self.rect.width - pos[0], self.rect.height - pos[1]))
            texts = []
            for i in self.texts.values():
                texts.extend(list(i.values()))
            for text in texts:
                text.draw(self.surface)

    def set_resources(self, resource: dict) -> None:
        self.resources = resource
        self.render_init()

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)


class InventoryRobot(Inventory):
    def __init__(self, pos: Tuple[int, int], width: int, height: int, max_items: int) -> None:
        self.max_items = max_items
        super().__init__(pos, width, height)

    def update(self, resource: str, condition: Union[str, bool] = False, quantity: int = 0) -> None:
        if type(condition) == bool:
            condition = 'продукт' if condition else 'сырьё'
        temp = self.resources[resource][condition] + quantity
        if sum([sum(i.values()) for i in self.resources.values()]) + quantity <= self.max_items and temp >= 0:
            self.resources[resource][condition] = temp
            self.texts[resource][condition].set_text(f'{self.resources[resource][condition]}')
            self.render()

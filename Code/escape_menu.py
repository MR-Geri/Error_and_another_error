from Code.settings import *
from Code.buttons import Button, Buttons
from Code.utils import Interface

from Code.texts import max_size_list_text, TextCenter


# Над файлом работала Катя. Я только менял что-то.
class EscMenu:
    def __init__(self, pos: Tuple[int, int], width: int, height: int, controller, save) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        self.surface.fill(COLOR_BACKGROUND)
        self.if_active: bool = False
        self.text = None
        self.save = save
        self.controller = controller
        self.interface = Interface(
            pos=(self.rect.x, self.rect.y), max_width=self.rect.width, max_height=self.rect.height,
            indent=(0, self.rect.height // 50), size=(self.rect.width, self.rect.height // 5)
        )
        #
        self.buttons = Buttons()
        self.init()

    def act_menu(self) -> None:
        self.if_active = False
        self.controller.action_window('menu')

    def act_settings(self) -> None:
        self.controller.action_window('settings')

    def resume(self) -> None:
        self.if_active = False

    def init(self) -> None:
        width, height = self.interface.width, self.interface.height
        data = [('Вернуться', self.resume), ('Настройки', self.act_settings),
                ('Сохранить игру', self.save), ('Главное меню', self.act_menu)]
        ind = len(data) * self.interface.height + len(data) * self.interface.indent[1]
        height_text = self.interface.max_height - ind
        self.text = TextMaxSizeCenter(text=f'Пауза', width=width, height=height_text, pos=self.interface.pos)
        self.interface.move(0, self.text.rect.height)
        size = max_size_list_text([i[0] for i in data], width=width, height=height, font_type=PT_MONO)
        for text, func in data[:-1]:
            button = Button(
                pos=self.interface.pos, width=width, height=height, func=func,
                color_disabled=(30, 30, 30), color_active=(40, 40, 40),
                text=TextCenter(text=text, width=width, height=height, font_type=PT_MONO, font_size=size)
            )
            self.buttons.add(button)
            self.interface.move(0)
        button = Button(
            pos=self.interface.pos, width=width, height=height, func=data[-1][1],
            color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(text=data[-1][0], width=width, height=height, font_type=PT_MONO, font_size=size)
        )
        self.buttons.add(button)

    def changes_active(self) -> None:
        self.if_active = not self.if_active

    def draw(self, surface: pg.Surface) -> None:
        if self.if_active:
            frame = pg.Surface((self.rect.width + 2 * self.interface.indent[1],
                                self.rect.height + 2 * self.interface.indent[1]))
            frame.fill(COLOR_BACKGROUND)
            surface.blit(frame, (self.rect.x - self.interface.indent[1], self.rect.y - self.interface.indent[1]))
            surface.blit(self.surface, self.rect)
            self.text.draw(surface)
            self.buttons.draw(surface)

    def event(self, event: pg.event.Event) -> None:
        self.buttons.event(event)

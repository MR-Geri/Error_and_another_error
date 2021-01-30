from Code.settings import *
from Code.Map.minimaps import Minimap
from Code.buttons import Buttons, Button, ButtonTwoStates
from Code.utils import Interface, Dial
from Code.sound import Music
from Code.texts import TextMaxSizeCenter, max_size_list_text


# Над файлом работал я.
class Panel:
    def __init__(self, width: int, height: int, pos: Tuple[int, int], pad: int, size: int) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.color_background = pg.Color((128, 128, 128))
        self.pad = pad
        self.size = size
        self.interface = Interface(
            pos=(0, self.rect.height // 70), max_width=width, max_height=height,
            indent=(0, self.rect.height // 100), size=(self.rect.width, (height - width) // 13)
        )

    def get_absolute_pos(self, x: int, y: int) -> Tuple[int, int]:
        return self.rect.x + x, self.rect.y + y

    def render(self) -> None:
        pass

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

    def update(self) -> None:
        pass

    def event(self, event: pg.event.Event) -> None:
        pass


class LeftPanel(Panel):
    def __init__(self, width: int, height: int, pos: Tuple[int, int], pad: int, size: int, music: Music = None) -> None:
        super().__init__(width, height, pos, pad, size)
        self.music = music
        # Миникарта
        self.minimap = Minimap(
            (self.pad, self.rect.height - self.pad - self.size), self.size, self.size)
        # Интерфейс
        self.buttons = None
        self.time = None
        self.running_line = None
        self.pos_cursor = None
        self.button_file = None
        self.button_del_file = None
        self.button_info = None
        self.processor = None
        self.dial = None
        #

    def init(self, processor) -> None:
        self.interface = Interface(
            pos=(0, self.rect.height // 70), max_width=self.rect.width, max_height=self.rect.height,
            indent=(0, self.rect.height // 100), size=(self.rect.width, (self.rect.height - self.rect.width) // 13)
        )
        self.buttons = Buttons()
        self.processor = processor
        self.init_interface()
        self.update()
        self.render()

    def init_interface(self) -> None:
        size = max_size_list_text(
            ['<', '>', '||', '►'], self.interface.width, self.interface.height, PT_MONO
        )
        width3, height = int(round(self.interface.width / 3, 0)), 2 * self.interface.height + self.interface.indent[1]
        self.dial = Dial(self.interface.pos, self.interface.height, UPDATE_CHANGE_TIME,
                         (255, 255, 255), (255, 255, 255))
        self.time = TextMaxSizeCenter(
            text=f"", width=self.interface.width - 4 * self.interface.height, height=self.interface.height,
            pos=(self.interface.pos[0] + self.interface.height, self.interface.pos[1]), font_type=PT_MONO
        )
        self.buttons.add(Button(
            pos=(self.interface.width - 3 * self.interface.height, self.interface.pos[1]),
            width=self.interface.height,
            height=self.interface.height,
            func=self.processor.down_speed, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextMaxSizeCenter(text='<', width=self.interface.height, height=self.interface.height,
                                   font_type=PT_MONO)
        ))
        self.buttons.add(ButtonTwoStates(
            pos=(self.interface.width - 2 * self.interface.height, self.interface.pos[1]), width=self.interface.height,
            height=self.interface.height,
            func=self.processor.change, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextMaxSizeCenter(text='||', width=self.interface.height, height=self.interface.height,
                                   font_type=PT_MONO),
            texts=('►', '||'), get_state=self.processor.get_state
        ))
        self.buttons.add(Button(
            pos=(self.interface.width - self.interface.height, self.interface.pos[1]), width=self.interface.height,
            height=self.interface.height,
            func=self.processor.up_speed, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextMaxSizeCenter(text='>', width=self.interface.height, height=self.interface.height,
                                   font_type=PT_MONO)
        ))
        self.interface.move(0)
        #
        self.running_line = RunningLineMaxSizeCenter(
            text='пример текста', width=self.interface.width, height=self.interface.height,
            pos=self.interface.pos, speed=30, font_type=PT_MONO
        )
        self.interface.move(0)
        button = Button(
            pos=self.interface.pos, width=width3, height=height,
            func=self.music.previous, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(
                text='<', width=width3, height=height, font_type=PT_MONO,
                font_size=size
            )
        )
        self.buttons.add(button)
        self.interface.move(button.rect.width, 0, is_indent=(False, False))
        button = ButtonTwoStates(
            pos=self.interface.pos, width=self.interface.width - 2 * width3, height=height,
            func=self.music.pause_and_play, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(text='||', width=self.interface.width - 2 * width3, height=height,
                            font_type=PT_MONO, font_size=size),
            texts=('►', '||'), get_state=self.music.get_state
        )
        self.buttons.add(button)
        self.interface.move(button.rect.width, 0, is_indent=(False, False))
        button = Button(
            pos=self.interface.pos, width=width3, height=height,
            func=self.music.next, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextCenter(
                text='>', width=width3, height=height, font_type=PT_MONO,
                font_size=size
            )
        )
        self.buttons.add(button)
        self.interface.move(- self.interface.width + width3, is_indent=(False, False))
        self.interface.move(0)
        self.pos_cursor = TextMaxSizeCenter(
            text='', width=self.interface.width, height=self.interface.height, pos=self.interface.pos, font_type=PT_MONO
        )
        self.interface.move(0)
        height2 = 2 * self.interface.height + self.interface.indent[1]
        self.button_info = Button(
            pos=self.interface.pos, width=self.interface.width, height=height2,
            func=None, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextMaxSizeCenter(text='Информация', width=self.interface.width,
                                   height=height2, font_type=PT_MONO)
        )
        self.interface.move(0, height2)
        self.button_file = Button(
            pos=self.interface.pos, width=self.interface.width, height=height2,
            func=None, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextMaxSizeCenter(text='Выбрать файл', width=self.interface.width,
                                   height=height2, font_type=PT_MONO)
        )
        self.interface.move(0, height2)
        self.button_del_file = Button(
            pos=self.interface.pos, width=self.interface.width, height=height2,
            func=None, color_disabled=(30, 30, 30), color_active=(40, 40, 40),
            text=TextMaxSizeCenter(text='Удалить файл', width=self.interface.width,
                                   height=height2, font_type=PT_MONO)
        )
        self.interface.move(0, height2)

    def update(self) -> None:
        self.running_line.update(self.music.get_text())
        if self.processor:
            self.time.set_text(f"{self.processor.tick_complete}")
        self.buttons.update_text()

    def update_cursor(self, pos_cursor: Tuple[int, int]) -> None:
        text = f'(x: {pos_cursor[0]}, y: {pos_cursor[1]})'
        if pos_cursor and text != self.pos_cursor.text:
            self.pos_cursor.set_text(text)

    def render_minimap(self, surface: pg.Surface, pos: Tuple[int, int] = None,
                       width: int = None, height: int = None) -> None:
        self.minimap.render(surface, pos, width, height)
        self.render()

    def render(self) -> None:
        self.surface.fill(self.color_background)
        #
        self.running_line.draw(self.surface)
        self.time.draw(self.surface)
        self.buttons.draw(self.surface)
        if self.button_file.func:
            self.button_file.draw(self.surface)
        if self.button_del_file.func:
            self.button_del_file.draw(self.surface)
        if self.button_info.func:
            self.button_info.draw(self.surface)
        if self.processor:
            self.dial.draw(self.surface, self.processor.tick_complete)
        self.minimap.draw(self.surface)
        self.pos_cursor.draw(self.surface)

    def event(self, event: pg.event.Event) -> None:
        self.buttons.event(event)
        if self.button_file.func:
            self.button_file.event(event)
        if self.button_del_file.func:
            self.button_del_file.event(event)
        if self.button_info.func:
            self.button_info.event(event)


class RightPanel(Panel):
    def __init__(self, width: int, height: int, pos: Tuple[int, int], pad: int, size: int) -> None:
        super().__init__(width, height, pos, pad, size)
        # Интерфейс
        self.info_update = None
        self.inventory_settings = (pos[0] + pad, self.rect.height - pad - size), size, size
        #
        self.counter_line = 10
        self.lines = []
        for _ in range(self.counter_line):
            self.lines.append(TextMaxSizeCenter(
                text='', width=self.interface.width - self.interface.width // 50, height=self.interface.height,
                pos=(self.interface.pos[0] + self.interface.width // 100, self.interface.pos[1]), font_type=PT_MONO
            ))
            self.interface.move(0)
        #
        self.update()
        self.render()

    def update(self) -> None:
        pass

    def update_text(self, texts: list = None) -> None:
        last = -1
        texts = list() if texts is None else texts
        for ind, text in enumerate(texts):
            if self.lines[ind].text != text:
                self.lines[ind].set_text(text)
            last = ind
        for ind in range(last + 1, self.counter_line):
            if self.lines[ind].text != '':
                self.lines[ind].set_text('')
        self.render()

    def render(self) -> None:
        self.surface.fill(self.color_background)
        #
        for line in self.lines:
            line.draw(self.surface)

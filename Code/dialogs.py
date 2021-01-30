from Code.scroll import Scroll
from Code.settings import *
from Code.buttons import Button
from Code.utils import Interface
from Code.line_input import LineInput
from Code.texts import max_size_list_text


# Над файлом работал я.
class DialogInfo:
    def __init__(self, pos: Tuple[int, int], width: int, height: int) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        self.surface.fill(pg.Color('#25B2B9'))
        width_ = self.rect.width - self.rect.width // 50
        self.button = Button(
            pos=(
                pos[0] + self.rect.width // 100,
                pos[1] + self.rect.height - self.rect.height // 5 - self.rect.height // 100
            ),
            width=width_, height=self.rect.height // 5,
            color_disabled=(30, 30, 30), color_active=(40, 40, 40), func=self.hide,
            text=TextMaxSizeCenter(text='Понятно', width=width_, height=self.rect.height // 5, font_type=PT_MONO)
        )
        self.if_active: bool = False

    def hide(self) -> None:
        self.if_active = False
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        self.surface.fill(pg.Color('#25B2B9'))

    def event(self, event: pg.event.Event) -> None:
        self.button.event(event)

    def show(self, texts: list) -> None:
        self.if_active = True
        interface = Interface(pos=(0, self.rect.height // 100), max_width=self.rect.width,
                              max_height=self.rect.height - self.rect.height // 10,
                              indent=(0, self.rect.height // 100), size=(self.rect.width, self.rect.height // 5))
        size = max_size_list_text(texts, interface.width, interface.height, font_type=PT_MONO)
        draw_texts = []
        for text in texts:
            draw_texts.append(TextCenter(text, width=interface.width, height=interface.height, pos=interface.pos,
                                         font_type=PT_MONO, font_size=size))
            interface.move(0)
        self.surface = pg.Surface(
            (self.rect.width, interface.pos[1] + interface.indent[1] + self.rect.height // 5), pg.SRCALPHA)
        self.surface.fill(pg.Color('#25B2B9'))
        for text in draw_texts:
            self.surface.blit(text.surface, text.rect)
        self.button = Button(
            pos=(
                self.rect.x + self.rect.width // 100,
                self.rect.y + interface.pos[1]
            ),
            width=self.rect.width - self.rect.width // 50, height=self.rect.height // 5,
            color_disabled=(30, 30, 30), color_active=(40, 40, 40), func=self.hide,
            text=TextMaxSizeCenter(text='Понятно', width=self.rect.width - self.rect.width // 50,
                                   height=self.rect.height // 5, font_type=PT_MONO)
        )

    def draw(self, surface: pg.Surface) -> None:
        if self.if_active:
            surface.blit(self.surface, self.rect)
            self.button.draw(surface)


class DialogFile:
    def __init__(self, pos: Tuple[int, int], width: int, height: int) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.fon = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        self.fon.fill(pg.Color(COLOR_BACKGROUND))
        self.if_active: bool = False
        self.path = None
        self.files = []
        #
        self.interface = Interface(pos=(pos[0] + width // 100, pos[1] + height // 50), max_width=width,
                                   max_height=height, indent=(0, height // 50),
                                   size=(int(0.98 * width), int(0.96 * height / 10)))
        self.line_input = LineInput(pos=self.interface.pos, width=self.interface.width, height=self.interface.height,
                                    font_type=PT_MONO, background_color=(60, 60, 60))
        self.line_text = TextMaxSizeCenter(text='Введите сюда полный путь до папки с кодом',
                                           pos=self.interface.pos, width=self.interface.width,
                                           height=self.interface.height, font_type=PT_MONO)
        self.interface.move(0)
        self.scroll = None

    def hide(self) -> None:
        self.if_active = False

    def event(self, event: pg.event.Event) -> None:
        if self.if_active:
            self.line_input.event(event)
            self.scroll.event(event)

    def show(self, line) -> None:
        self.scroll = Scroll(pos=self.interface.pos, width=self.interface.width, one_line=self.interface.height,
                             height=9 * self.interface.height, color=COLOR_BACKGROUND, if_button=True, line=line,
                             color_disabled=(128, 128, 128), color_active=(138, 138, 138), path=self.line_input)
        self.if_active = True
        self.line_input.if_active = True
        self.files = []

    def draw(self, surface: pg.Surface) -> None:
        if self.if_active:
            surface.blit(self.fon, self.rect)
            self.line_input.draw(surface)
            if self.line_input.text.text == '':
                self.line_text.draw(surface)
            self.scroll.draw(surface)
            if not self.line_input.if_active and self.line_input.text.text != '':
                self.path = self.line_input.text.text.replace('/', r'\ '[0])
                if self.path[-1] != r'\ '[0]:
                    self.path += r'\ '[0]
                try:
                    files = [[i for i in files] for root, _, files in walk(self.path[:-1])][0]
                    if files != self.files:
                        self.scroll.update([
                            TextMaxSizeCenter(text=f, width=self.interface.width, height=self.interface.height,
                                              font_type=PT_MONO)
                            for f in files])
                        self.files = list(files)
                except Exception as e:
                    print(f'Load files users -> Exception: {e}')


class DialogCodeUse:
    def __init__(self, pos: Tuple[int, int], width: int, height: int, dialog_info: DialogInfo, sector) -> None:
        self.sector = sector
        self.dialog_info = dialog_info
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.surface.Surface((width, height))
        self.if_active: bool = False
        self.interface = Interface(pos=(0, 0), max_width=width, max_height=height, indent=(0, height // 10),
                                   size=(width, int(height * (4/5) / 3)))
        self.text = TextMaxSizeCenter('Разовый код', pos=self.interface.pos, width=self.interface.width,
                                      height=self.interface.height)
        self.interface.move(0)
        self.line_input = LineInput(pos=self.interface.pos, width=self.interface.width, height=self.interface.height,
                                    font_type=PT_MONO, offset=pos, background_color=(40, 40, 40))
        self.interface.move(0)
        self.button = Button(pos=self.interface.pos, width=self.interface.width,
                             height=self.interface.height, func=self.processing_read, offset=pos,
                             text=TextMaxSizeCenter('Применить', width=self.interface.width,
                                                    height=self.interface.height),
                             color_disabled=(30, 30, 30), color_active=(40, 40, 40))
        self.render()

    @staticmethod
    def read(line_input, dialog_info, place_base, create_robot, place_foundry):
        from Code.sector_objects.robots import MK0, MK1, MK2, MK3
        t = line_input.text.text
        try:
            eval(str(t))
        except SyntaxError:
            exec(str(t))
        except NameError:
            dialog_info.show([f'Не существует такого объекта'])
        except Exception as e:
            print(e)
            dialog_info.show([f'Нет такой команды'])

    def processing_read(self) -> None:
        self.read(self.line_input, self.dialog_info, self.sector.place_base, self.sector.create_robot,
                  self.sector.place_foundry)
        self.sector.render()
        self.if_active = False

    def render(self) -> None:
        self.surface.fill(pg.Color((30, 30, 30)))
        self.text.draw(self.surface)

    def draw(self, surface: pg.surface.Surface) -> None:
        if self.if_active:
            self.button.draw(self.surface)
            self.line_input.draw(self.surface)
            surface.blit(self.surface, self.rect)

    def changes_active(self) -> None:
        self.line_input.clear()
        self.line_input.if_active = True
        self.if_active = not self.if_active

    def event(self, event: pg.event.Event) -> None:
        if self.if_active:
            self.line_input.event(event)
            self.button.event(event)


class DialogState:
    def __init__(self, pos: Tuple[int, int], width: int, height: int) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        self.surface.fill(COLOR_BACKGROUND)
        x = width // 100
        self.scroll = Scroll(pos=(pos[0] + x, pos[1]), width=width - x,
                             height=int(self.rect.height * 4/5), one_line=self.rect.height // 5,
                             color=COLOR_BACKGROUND, color_disabled=(128, 128, 128), color_active=(138, 138, 138))
        self.button = Button(
            pos=(pos[0], pos[1] + int(self.rect.height * 4/5) + 1), width=width, height=self.rect.height // 5,
            color_disabled=(30, 30, 30), color_active=(40, 40, 40), func=self.hide,
            text=TextMaxSizeCenter(text='Понятно', width=width, height=self.rect.height // 5, font_type=PT_MONO)
        )
        self.if_active: bool = False

    def hide(self) -> None:
        self.if_active = False
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        self.surface.fill(COLOR_BACKGROUND)
        self.scroll.clear()

    def event(self, event: pg.event.Event) -> None:
        self.button.event(event)
        self.scroll.event(event)

    def show(self, texts: list) -> None:
        self.if_active = True
        self.scroll.update(texts)

    def draw(self, surface: pg.Surface) -> None:
        if self.if_active:
            surface.blit(self.surface, self.rect)
            self.button.draw(surface)
            self.scroll.draw(surface)

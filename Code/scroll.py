from Code.texts import Texts
from Code.utils import Interface
from Code.settings import *
from Code.buttons import ChoiceButton, Buttons
from Code.slider import VerticalSlider, Numbers


# Над файлом работала Катя.
class Scroll:
    def __init__(self, pos: Tuple[int, int], width: int, one_line: int, height: int, color: COLOR,
                 if_button: bool = False, color_disabled: COLOR = (30, 30, 30),
                 color_active: COLOR = (40, 40, 40), line=None, path=None) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.surface = pg.Surface((self.rect.width, self.rect.height))
        self.color = color
        self.surface.fill(self.color)
        self.if_button = if_button
        self.color_active = color_active
        self.color_disabled = color_disabled
        self.one_line = one_line
        self.line = line
        self.path = path
        #
        self.buttons = Buttons()
        self.texts = Texts()
        self.position = Numbers(0, 100, self.one_line // 2)
        self.slider = VerticalSlider(
            pos=(int(self.rect.width * 0.95), 0), width=int(self.rect.width * 0.05), height=self.rect.height,
            color_no_use=COLOR_SLIDER_NO_USE,
            color_use=COLOR_SLIDER_NO_USE,
            color_circle=COLOR_SLIDER_CIRCLE,
            slider=self.position,
            func=None,
            offset=(self.rect.x, self.rect.y)
        )

    def clear(self) -> None:
        self.buttons = Buttons()
        self.texts = Texts()
        self.position.set_value(0)

    def update(self, texts: list) -> None:
        self.buttons = Buttons()
        self.texts = Texts()
        pos_text = Interface(
            pos=(0, 0), max_width=self.rect.width, max_height=None, size=(int(self.rect.width * 0.94), self.one_line),
            indent=(self.one_line // 10, self.one_line // 10))
        for text in texts:
            if self.if_button:
                self.buttons.add(ChoiceButton(
                    text=text, pos=pos_text.pos, width=pos_text.width, height=pos_text.height, line=self.line,
                    path=self.path, color_active=self.color_active, color_disabled=self.color_disabled,
                    offset=(self.rect.x, self.rect.y)))
            else:
                self.texts.add(TextMaxSizeCenter(
                    text=text, pos=pos_text.pos, width=pos_text.width, height=pos_text.height, font_type=PT_MONO))
            pos_text.move(0, is_indent=(False, True))
        self.position.set(0, pos_text.pos[1] - self.rect.height)

    def draw(self, surface: pg.Surface) -> None:
        self.surface.fill(self.color)
        if self.if_button:
            objs = self.buttons.buttons
        else:
            objs = self.texts.texts
        for obj in objs:
            self.surface.blit(obj.surface, (obj.rect.x, obj.rect.y - self.position.value))
        self.slider.draw(self.surface)
        surface.blit(self.surface, self.rect)

    def event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONUP and event.button == 4:
            self.position.edit(-1)
        if event.type == pg.MOUSEBUTTONUP and event.button == 5:
            self.position.edit(1)
        self.slider.event(event)
        if self.if_button:
            self.buttons.event(event, correction=(0, self.position.value))

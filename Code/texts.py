from typing import Tuple
import pygame as pg


# Над файлом работал я.
def print_text(display, text: str, pos: Tuple[int, int], font_color: Tuple[int, int, int] = (255, 0, 0),
               font_size: int = 20) -> None:
    font = pg.font.Font(None, font_size)
    text = font.render(text, True, font_color)
    text_rect = text.get_rect()
    text_rect.x, text_rect.y = pos
    display.blit(text, text_rect)


def max_size_list_text(texts: list, width: int, height: int, font_type: str = None) -> int:
    size = list()
    for text in texts:
        size.append(TextMaxSize(text=text, width=width, height=height, font_type=font_type).font_size)
    return min(size)


class Text:
    def __init__(self, text: str, pos: Tuple[int, int] = (0, 0), font_color: Tuple[int, int, int] = (255, 255, 255),
                 font_type: str = None, font_size: int = 20) -> None:
        self.text = text
        self.pos = tuple(pos)
        self.font_color = font_color
        self.font_type = font_type
        self.font_size = font_size
        #
        self.font = pg.font.Font(font_type, font_size)
        self.surface = self.font.render(text, True, font_color)
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = self.pos

    def set_text(self, text: str) -> None:
        if text != self.text:
            self.text = text
            self.__init__(text=text, pos=self.pos, font_color=self.font_color, font_type=self.font_type,
                          font_size=self.font_size)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)


class TextMaxSize:
    def __init__(self, text: str,  width: int = None, height: int = None, pos: Tuple[int, int] = (0, 0),
                 font_color: Tuple[int, int, int] = (255, 255, 255), font_type: str = None) -> None:
        self.width = int(width) if width is not None else None
        self.height = int(height) if height is not None else None
        self.text = text
        self.pos = tuple(pos)
        self.font_color = font_color
        self.font_type = font_type
        self.font_size = 1
        while True:
            self.surface = pg.font.Font(font_type, self.font_size).render(text, True, font_color)
            self.rect = self.surface.get_rect()
            if (width and width <= self.rect.width) or (height and height <= self.rect.height):
                self.font_size -= 1
                self.surface = pg.font.Font(font_type, self.font_size).render(text, True, font_color)
                self.rect = self.surface.get_rect()
                self.rect.x, self.rect.y = pos
                break
            self.font_size += 1

    def set_text(self, text: str) -> None:
        if text != self.text:
            self.text = text
            self.__init__(text, self.width, self.height, self.pos, self.font_color, self.font_type)

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)


class TextMaxSizeCenter(TextMaxSize):
    def __init__(self, text: str, width: int = None, height: int = None, pos: Tuple[int, int] = (0, 0),
                 font_color: Tuple[int, int, int] = (255, 255, 255), font_type: str = None) -> None:
        super().__init__(text=text, pos=pos, width=width, height=height, font_color=font_color, font_type=font_type)
        if width:
            self.rect.x += (width - self.rect.width) // 2
        if height:
            self.rect.y += (height - self.rect.height) // 2


class TextCenter(Text):
    def __init__(self, text: str, width: int = None, height: int = None, pos: Tuple[int, int] = (0, 0),
                 font_color: Tuple[int, int, int] = (255, 255, 255),
                 font_type: str = None, font_size: int = 20) -> None:
        self.width = width
        self.height = height
        super().__init__(text=text, pos=pos, font_color=font_color, font_type=font_type, font_size=font_size)
        if width:
            self.rect.x += (width - self.rect.width) // 2
        if height:
            self.rect.y += (height - self.rect.height) // 2

    def set_text(self, text: str, font_size: int = None) -> None:
        if text != self.text:
            self.text = text
            self.__init__(text=text, width=self.width, height=self.height, pos=self.pos, font_color=self.font_color,
                          font_type=self.font_type, font_size=font_size if font_size else self.font_size)


class Texts:
    def __init__(self) -> None:
        self.texts = []

    def add(self, text) -> None:
        self.texts.append(text)

    def draw(self, surface: pg.Surface) -> None:
        for text in self.texts:
            text.draw(surface)

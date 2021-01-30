from Code.settings import *

from typing import Tuple
import pygame as pg
import numpy as np


# Над файлом работал я.
class Matrix:
    def __init__(self, pos: Tuple[int, int], width: int, height: int, path: str, font_size=8):
        self.surface = pg.Surface((width, height))
        self.rect = pg.Rect(*pos, width, height)
        self.FONT_SIZE = font_size
        self.SIZE = self.ROWS, self.COLS = height // font_size, width // font_size
        self.katakana = np.array([chr(int('0x30a0', 16) + i) for i in range(96)] + ['' for _ in range(10)])
        self.font = pg.font.Font(MS_MINCHO, font_size, bold=True)

        self.matrix = np.random.choice(self.katakana, self.SIZE)
        self.char_intervals = np.random.randint(25, 50, size=self.SIZE)
        self.cols_speed = np.random.randint(100, 250, size=self.SIZE)
        self.prerendered_chars = self.get_prerendered_chars()
        self.image = self.get_image(path)

    def get_image(self, path_to_file):
        image = pg.image.load(path_to_file)
        image = pg.transform.scale(image, (self.rect.width, self.rect.height))
        pixel_array = pg.pixelarray.PixelArray(image)
        return pixel_array

    def get_prerendered_chars(self):
        char_colors = [(color, color, color) for color in range(256)]
        prerendered_chars = {}
        for char in self.katakana:
            prerendered_char = {(char, color): self.font.render(char, True, color) for color in char_colors}
            prerendered_chars.update(prerendered_char)
        return prerendered_chars

    def draw(self, display: pg.Surface):
        frames = pg.time.get_ticks()
        self.change_chars(frames)
        self.shift_column(frames)
        self.render()
        display.blit(self.surface, self.rect)

    def shift_column(self, frames):
        num_cols = np.argwhere(frames % self.cols_speed == 0)
        num_cols = num_cols[:, 1]
        num_cols = np.unique(num_cols)
        self.matrix[:, num_cols] = np.roll(self.matrix[:, num_cols], shift=1, axis=0)

    def change_chars(self, frames):
        mask = np.argwhere(frames % self.char_intervals == 0)
        new_chars = np.random.choice(self.katakana, mask.shape[0])
        self.matrix[mask[:, 0], mask[:, 1]] = new_chars

    def render(self):
        self.surface.fill(pg.Color('black'))
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char:
                    pos = x * self.FONT_SIZE, y * self.FONT_SIZE
                    _, red, green, blue = pg.Color(self.image[pos])
                    if red and green and blue:
                        color = (red + green + blue) // 3
                        color = 220 if 160 < color < 220 else color
                        char = self.prerendered_chars[(char, (color, color, color))]
                        char.set_alpha(color + 60)
                        self.surface.blit(char, pos)

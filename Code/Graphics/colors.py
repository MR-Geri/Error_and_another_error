from random import randint
import pygame as pg


def pg_random_color() -> pg.Color:
    return pg.Color((randint(0, 255), randint(0, 255), randint(0, 255)))

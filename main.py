from Code.controller import Controller
import pygame as pg

if __name__ == '__main__':
    pg.mixer.pre_init(44100, -16, 1, 512)
    pg.init()
    controller = Controller()
    controller.menu.run()

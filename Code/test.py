import time
from Game_code import robot
import importlib


class Test:
    def __init__(self):
        self.x = 1

    @staticmethod
    def func():
        return 1

    def my_func(self):
        p = self.func()
        print('p =', p)


if __name__ == '__main__':
    test = Test()
    for i in range(12):
        print(i)
        try:
            importlib.reload(importlib.import_module('Game_code.robot_move'))
            print(importlib.import_module('Game_code.robot_move').func())
        except Exception as e:
            print('Ошибка', e)
        time.sleep(2)

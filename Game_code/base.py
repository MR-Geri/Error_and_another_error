from const import *
from typing import Union


def energy_transfer(state, board, entities) -> Union[list, None]:
    robots = []
    pos = state['pos']
    for y in range(pos[1] - state['distance_charging'], pos[1] + state['distance_charging'] + 1):
        for x in range(pos[0] - state['distance_charging'], pos[0] + state['distance_charging'] + 1):
            if state['pos'] != (x, y) and state['permissions'].can_charging and state['energy'] > 200:
                robot = entities[y][x]
                if robot:
                    if robot['energy'] < robot['energy_max']:
                        robots.append((5, (x, y)))
                        if robot['name'] in ROBOTS:
                            robot['permissions'].set_move(False)
                        elif robot['name'] in ROBOTS:
                            robot['permissions'].set_move(True)
    return robots if robots else None


def item_transfer(state, board, entities):
    pos = 22, 4
    invent = state['inventory']
    for element in invent:
        if invent[element]['сырьё'] > 0:
            return pos, element, 'сырьё', 50
    return None

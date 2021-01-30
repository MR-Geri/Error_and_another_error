from typing import Tuple, Union
from const import *


def move(state, board, entities) -> Union[Tuple[int, int], None]:
    pos = state['pos']
    if state['energy'] <= state['energy_max'] // 2 or \
            sum([sum(i.values()) for i in state['inventory'].values()]) == state['inventory_max']:
        return pos[0] - 1, pos[1]
    return pos[0] + 1, pos[1]


def mine(state, board, entities) -> Union[Tuple[int, int], None]:
    pos = state['pos']
    if sum([sum(i.values()) for i in state['inventory'].values()]) < state['inventory_max'] and \
            board[pos[1]][pos[0] + 1]['name'] in ORES and state['energy'] > 100:
        state['permissions'].can_move = False
        return pos[0] + 1, pos[1]
    state['permissions'].can_move = True
    return None


def item_transfer(state, board, entities):
    invent = state['inventory']
    for element in invent:
        for i in invent[element]:
            if invent[element][i] > 0:
                return (12, 14), element, i, invent[element][i]
    return None

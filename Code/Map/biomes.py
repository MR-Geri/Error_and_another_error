from Code.settings import *
from Code.info_panel import RightPanel

from collections import defaultdict


# Над файлом работал я.
class Biome:
    def __init__(self, number_x: int, number_y: int, max_size_biome: Tuple[int, int], min_quantity: int,
                 size_cell: int, cell: ALL_CELL, right_panel: RightPanel) -> None:
        self.number_x = number_x
        self.number_y = number_y
        self.max_size_biome = max_size_biome
        self.cell = cell
        self.size_cell = size_cell
        self.right_panel = right_panel
        #
        self.number_xy = (randint(1, self.max_size_biome[0]), randint(1, self.max_size_biome[1]))
        self.size = randint(min_quantity, self.max_size_biome[0] * self.max_size_biome[1])
        self.pos = (
            randint(self.number_xy[0], self.number_x - self.number_xy[0]),
            randint(self.number_xy[1], self.number_y - self.number_xy[1])
        )
        #
        self.cells, self.cords_cells = self.gen_all_cell()

    def new_possible(self, possible: list, pos: Tuple[int, int]) -> list:
        x, y = pos
        possible.remove(pos)
        for _x, _y in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if 0 <= _x <= self.number_xy[0] + self.pos[0] and 0 <= _y <= self.number_xy[1] + self.pos[1]:
                possible.append((_x, _y))
        return possible

    def gen_all_cell(self) -> Tuple[defaultdict, set]:
        cells, cords_cells = defaultdict(lambda: defaultdict()), set()
        pos_0 = self.pos[0] + self.number_xy[0] // 2, self.pos[1] + self.number_xy[1] // 2
        possible = self.new_possible([pos_0], pos_0)
        for i in range(self.size):
            pos = choice(possible)
            possible = self.new_possible(possible, pos)
            cells[pos[1]][pos[0]] = self.cell(*pos, self.size_cell, self.right_panel)
            cords_cells.add(pos)
        return cells, cords_cells


class GeneratorBiomes:
    def __init__(self, number_x: int, number_y: int, size_cell: int, right_panel: RightPanel):
        self.number_x = number_x
        self.number_y = number_y
        self.size_cell = size_cell
        self.right_panel = right_panel
        #
        self.mountain = []
        self.swamp = []
        self.desert = []
        self.iron_ore = []
        self.aluminium_ore = []
        self.gold_ore = []
        self.cooper_ore = []
        self.tin_ore = []
        self.silicon_ore = []
        self.platinum_ore = []
        self.for_biomes = [
            (MAX_QUANTITY_MOUNTAIN, MIN_QUANTITY_MOUNTAIN_CELL, MAX_SIZE_MOUNTAIN, Mountain, self.mountain),
            (MAX_QUANTITY_SWAMP, MIN_QUANTITY_SWAMP_CELL, MAX_SIZE_SWAMP, Swamp, self.swamp),
            (MAX_QUANTITY_DESERT, MIN_QUANTITY_DESERT_CELL, MAX_SIZE_DESERT, Desert, self.desert),
            (MAX_QUANTITY_IRON, MIN_QUANTITY_IRON_CELL, MAX_SIZE_IRON, IronOre, self.iron_ore),
            (MAX_QUANTITY_ALUMINIUM, MIN_QUANTITY_ALUMINIUM_CELL, MAX_SIZE_ALUMINIUM, AluminiumOre, self.aluminium_ore),
            (MAX_QUANTITY_GOLD, MIN_QUANTITY_GOLD_CELL, MAX_SIZE_GOLD, GoldOre, self.gold_ore),
            (MAX_QUANTITY_COOPER, MIN_QUANTITY_COOPER_CELL, MAX_SIZE_COOPER, CooperOre, self.cooper_ore),
            (MAX_QUANTITY_TIN, MIN_QUANTITY_TIN_CELL, MAX_SIZE_TIN, TinOre, self.tin_ore),
            (MAX_QUANTITY_SILICON, MIN_QUANTITY_SILICON_CELL, MAX_SIZE_SILICON, SiliconOre, self.silicon_ore),
            (MAX_QUANTITY_PLATINUM, MIN_QUANTITY_PLATINUM_CELL, MAX_SIZE_PLATINUM, PlatinumOre, self.platinum_ore)
        ]
        #
        self.biomes = []
        self.gen_biomes()

    def get_cell(self, x: int, y: int) -> ALL_CELL:
        # Можно переделать на ХЕШ таблицы (словари)
        for group in self.biomes:
            for biome_ in group:
                if (x, y) in biome_.cords_cells:
                    return biome_.cells[y][x]
        return Plain(x, y, self.size_cell, self.right_panel)

    def entering_biome(self, biome) -> bool:
        # Можно переделать на ХЕШ таблицы (словари)
        for group in self.biomes:
            for biome_ in group:
                if biome.cords_cells.intersection(biome_.cords_cells):
                    return False
        return True

    def gen_biomes(self) -> None:
        for quantity, min_quantity, max_size_biome, cell, link_biome in self.for_biomes:
            for i in range(quantity):
                while True:
                    temp_biome = Biome(self.number_x, self.number_y, max_size_biome, min_quantity, self.size_cell,
                                       cell, self.right_panel)
                    if self.entering_biome(temp_biome):
                        break
                link_biome.append(temp_biome)
            self.biomes.append(link_biome)

from Code.settings import *


# Над файлом работал я.
class RadioisotopeGenerator:
    def __init__(self, generation_energy, resource: int = 10 ** 6) -> None:
        self.generation_energy = generation_energy
        self.energy_generate = 15
        self.energy_tick = 1
        self.resource = resource
        #
        self.name = 'Радиоизотопный генератор'

    def update(self, tick: int) -> None:
        if not tick % self.energy_tick and self.resource:
            self.resource -= self.energy_generate
            self.generation_energy(self.energy_generate)

    def draw(self, surface: pg.Surface, rect: pg.Rect) -> None:
        pos = (rect.width // 2, rect.height // 2)
        radius = rect.width // 4
        pg.draw.circle(surface, pg.Color('#A10C00'), pos, radius)

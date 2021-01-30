from Code.settings import *
from Code.sound import Sound


# Над файлом работал я.
class Entities:
    def __init__(self, sector_size: Tuple[int, int], sound: Sound) -> None:
        self.sound = sound
        self.sector_size = sector_size
        self.entities_sector = {y: {x: None for x in range(self.sector_size[0])} for y in range(self.sector_size[1])}

    def add(self, entity) -> None:
        x, y = entity.pos
        if self.entities_sector[y][x]:
            self.sound.add(self.entities_sector[y][x].sound_crash)
        self.entities_sector[y][x] = entity

    def draw(self, surface: pg.Surface) -> None:
        for y in self.entities_sector:
            for x in self.entities_sector[y]:
                entity = self.entities_sector[y][x]
                if entity is not None:
                    entity.draw(surface)

    def scale(self, size_cell: int) -> None:
        for y in self.entities_sector:
            for x in self.entities_sector[y]:
                entity = self.entities_sector[y][x]
                if entity is not None:
                    entity.scale(size_cell)

    def save(self) -> list:
        save = []
        for y in self.entities_sector:
            for x in self.entities_sector[y]:
                entity = self.entities_sector[y][x]
                if entity is not None:
                    save.append(entity.save())
        return save

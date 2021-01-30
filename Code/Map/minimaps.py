from Code.settings import *


# Над файлом работал я.
class Minimap:
    def __init__(self, pos: Tuple[int, int], width: int, height: int) -> None:
        self.surface = pg.Surface((width, height))
        self.surface.fill((0, 0, 0))
        self.rect = pg.Rect(*pos, width, height)

    def render(self, surface: pg.Surface, pos: Tuple[int, int] = None, width: int = None, height: int = None) -> None:
        self.surface = surface.copy()
        if pos:
            pg.draw.rect(self.surface, pg.Color((255, 255, 255)), pg.Rect(*pos, width, height), 15)
        self.surface = pg.transform.scale(self.surface, (self.rect.width, self.rect.height))
        # self.surface.fill((0, 0, 0))

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)

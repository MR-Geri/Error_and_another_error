from typing import Tuple


# Над файлом работал я.
class Permission:
    def __init__(self, active: Tuple[int, int]) -> None:
        self.permissions = [
            (640, 480), (960, 540), (1280, 720), (1280, 768), (1280, 1024), (1440, 1080), (1536, 960),
            (1536, 1024), (1600, 1024), (1920, 1080), (2048, 1080), (2048, 1152), (2048, 1536),
            (2560, 1080), (2560, 1440), (2560, 1600), (2560, 2048), (3200, 1800), (3200, 2048),
            (3200, 2400), (3440, 1440), (3840, 2160), (3840, 2400), (4096, 2160)
        ]
        self.active = active

    def next(self) -> None:
        self.active = self.permissions[(self.permissions.index(self.active) + 1) % (len(self.permissions) + 1)]

    def previous(self) -> None:
        ind = self.permissions.index(self.active) - 1 + len(self.permissions)
        self.active = self.permissions[ind % len(self.permissions)]

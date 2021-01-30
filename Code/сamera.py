from Code.settings import *


# Над файлом работал я.
class Camera:
    def __init__(self, width: int, height: int, left: int, right: int, win_width: int, win_height: int,
                 speed_x: int, speed_y: int) -> None:
        self.width = width
        self.height = height
        self.left = left
        self.right = right
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.win_width, self.win_height = win_width, win_height
        self.rect = pg.Rect((self.win_width - self.width) // 2, (self.win_height - self.height) // 2, width, height)
        self.move_x, self.move_y = 0, 0

    def get_cord(self) -> Tuple[int, int]:
        return self.rect.x, self.rect.y

    def move(self, left: bool, right: bool, up: bool, down: bool) -> None:
        self.move_x, self.move_y = 0, 0
        max_width, max_height = self.win_width - self.width, self.win_height - self.height
        if left:
            self.move_x += self.speed_x
        if right:
            self.move_x -= self.speed_x
        if up:
            self.move_y += self.speed_y
        if down:
            self.move_y -= self.speed_y
        if -max_width + self.left >= -(self.rect.x + self.move_x) >= -self.left:
            self.rect.x += self.move_x
        if -max_height >= -(self.rect.y + self.move_y) >= 0:
            self.rect.y += self.move_y

    def save(self, k: Union[int, float]) -> Tuple[float, float, float, float]:
        return self.rect.x / k, self.rect.y / k, self.rect.width / k, self.rect.height / k

    def load(self, data: Tuple[float, float, float, float], k: Union[int, float]) -> None:
        self.rect = pg.Rect(int(data[0] * k), int(data[1] * k), int(data[2] * k), int(data[3] * k))

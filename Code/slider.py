from Code.settings import *


# Над файлом работал я. И что-то делала Катя, но я уже не помню.
class Numbers:
    def __init__(self, min_value: Union[int, float], max_value: Union[int, float], change: Union[int, float],
                 value: Union[int, float] = None) -> None:
        self.min_value = min_value
        self.max_value = max_value
        self.change = change
        self.value = value if value is not None else min_value

    def edit(self, sign) -> None:
        self.value = min(self.max_value, max(self.min_value, self.value + sign * self.change))

    def set_value(self, value) -> None:
        self.value = min(self.max_value, max(self.min_value, value))

    def set(self, min_value: Union[int, float], max_value: Union[int, float]) -> None:
        self.min_value, self.max_value = min_value, max_value


class Slider:
    def __init__(self, pos: Tuple[int, int], width: int, height: int, color_no_use: COLOR, color_use: COLOR,
                 color_circle: COLOR, slider, func, offset: Tuple[int, int] = None, name: str = None) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.click = pg.Rect(*pos, width, height)
        if offset:
            self.click.x, self.click.y = self.click.x + offset[0], self.click.y + offset[1]
        self.slider = slider
        self.func = func
        self.name = name
        self.color_no_use = color_no_use
        self.color_use = color_use
        self.color_circle = color_circle
        # Отрисовка
        self.radius_main, self.rect_height = int(self.rect.height / 2), int(self.rect.height / 2.5)
        self.radius_mini = int(self.rect_height / 2)
        self.two_radius = self.radius_main + self.radius_mini
        self.rect_width = int(self.rect.width - 2 * self.radius_main - 2 * self.radius_mini)
        self.padding = int((self.rect.height - self.rect_height) / 2)
        self.pixel_size = self.rect_width + 2 * self.radius_mini
        self.pixel_change = self.pixel_size / self.slider.max_value * self.slider.change
        #
        self.flag_click = False
        self.render()

    def event(self, event: pg.event.Event) -> None:
        try:
            if self.click.collidepoint(*event.pos):
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    self.flag_click = False
                if self.flag_click:
                    value = round(
                        (event.pos[0] - self.click.x - self.radius_main) / self.pixel_change * self.slider.change, 3
                    )
                    self.slider.set_value(value)
                    # print(self.slider.value)
                    if self.func:
                        if self.name:
                            self.func.update(self.slider.value, self.name)
                        else:
                            self.func.update(self.slider.value)
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.flag_click:
                    self.flag_click = True
            else:
                self.flag_click = False
            self.render()
        except AttributeError:
            pass

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        pg.draw.circle(
            self.surface, self.color_use, (self.two_radius, self.padding + self.radius_mini), self.radius_mini
        )
        pg.draw.circle(
            self.surface, self.color_no_use,
            (self.rect.width - self.two_radius, self.padding + self.radius_mini), self.radius_mini
        )
        pg.draw.rect(
            self.surface, self.color_no_use, (self.two_radius, self.padding, self.rect_width, self.rect_height)
        )
        w_value = self.pixel_size * (self.slider.value / self.slider.max_value)
        pg.draw.rect(self.surface, self.color_use, (self.two_radius, self.padding, w_value, self.rect_height))
        pg.draw.circle(
            self.surface, self.color_circle,
            (self.radius_main + w_value, self.padding + self.radius_mini), self.radius_main
        )

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)


class VerticalSlider:
    def __init__(self, pos: Tuple[int, int], width: int, height: int, color_no_use: COLOR, color_use: COLOR,
                 color_circle: COLOR, slider, func, offset: Tuple[int, int] = None) -> None:
        self.rect = pg.Rect(*pos, width, height)
        self.click = pg.Rect(*pos, width, height)
        if offset:
            self.click.x, self.click.y = self.click.x + offset[0], self.click.y + offset[1]
        self.slider = slider
        self.func = func
        self.color_no_use = color_no_use
        self.color_use = color_use
        self.color_circle = color_circle
        # Отрисовка
        self.radius_main, self.rect_width = int(self.rect.width / 2), int(self.rect.width / 2.5)
        self.radius_mini = int(self.rect_width / 2)
        self.two_radius = self.radius_main + self.radius_mini
        self.rect_height = int(self.rect.height - 2 * self.radius_main - 2 * self.radius_mini)
        self.padding = int((self.rect.width - self.rect_width) / 2)
        self.pixel_size = self.rect_height + 2 * self.radius_mini
        #
        self.flag_click = False
        self.render()

    def event(self, event: pg.event.Event) -> None:
        pixel_change = self.pixel_size / self.slider.max_value * self.slider.change
        try:
            if self.click.collidepoint(*event.pos):
                if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    self.flag_click = False
                if self.flag_click:
                    value = round(
                        (event.pos[1] - self.click.y - self.radius_main) / pixel_change * self.slider.change, 3
                    )
                    self.slider.set_value(value)
                    # print(self.slider.value)
                    if self.func:
                        self.func.update(self.slider.value)
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.flag_click:
                    self.flag_click = True
            else:
                self.flag_click = False
            self.render()
        except AttributeError:
            pass

    def render(self) -> None:
        self.surface = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        # закруглённые края
        pg.draw.circle(
            self.surface, self.color_use, (self.padding + self.radius_mini, self.two_radius), self.radius_mini
        )
        pg.draw.circle(
            self.surface, self.color_no_use,
            (self.padding + self.radius_mini, self.rect.height - self.two_radius), self.radius_mini
        )
        #
        pg.draw.rect(
            self.surface, self.color_no_use, (self.padding, self.two_radius, self.rect_width, self.rect_height)
        )
        h_value = self.pixel_size * (self.slider.value / self.slider.max_value)
        pg.draw.rect(self.surface, self.color_use, (self.padding, self.two_radius, self.rect_width, h_value))
        pg.draw.circle(
            self.surface, self.color_circle,
            (self.padding + self.radius_mini, self.radius_main + h_value), self.radius_main
        )

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.surface, self.rect)


class Sliders:
    def __init__(self) -> None:
        self.sliders = []

    def add(self, button: Union[Slider, VerticalSlider]) -> None:
        self.sliders.append(button)

    def event(self, event: pg.event.Event) -> None:
        for slider in self.sliders:
            slider.event(event)

    def draw(self, surface: pg.Surface) -> None:
        for slider in self.sliders:
            slider.draw(surface)

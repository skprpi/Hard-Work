from ast import Tuple
from enum import Enum


class WindowInfo:
    def __init__(self, fps: int, weight: int, heigh: int):
        self._fps = fps
        self._weight = weight
        self._heigh = heigh

    def get_fps(self):
        return self._fps

    def get_screen_size(self):# -> Tuple[int, int]:
        return (self._weight, self._heigh)


class ColorManager(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

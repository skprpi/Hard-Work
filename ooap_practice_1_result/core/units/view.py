import pygame
from abc import ABC, abstractmethod
from typing import Tuple


class UnitView(ABC):
    def __init__(self, color: Tuple[int, int, int], shape: pygame.sprite.Sprite, window):
        self._color = color
        self._shape = shape
        self._window = window

    @abstractmethod
    def draw(self):
        ...

    @abstractmethod
    def set_position(self, position: Tuple[float, float]):
        ...

    @abstractmethod
    def get_position(self) -> Tuple[float, float]:
        ...

    @abstractmethod
    def get_rect(self) -> pygame.rect.Rect:
        ...


class RectangleUnitView(UnitView):
    def __init__(self, position: Tuple[float, float], width: int, heigh: int, color: Tuple[int, int, int], window):
        view = pygame.sprite.Sprite()
        view.rect = pygame.Rect(position[0], position[1], width, heigh)
        super().__init__(color, view, window)

    def draw(self):
        pygame.draw.rect(self._window, self._color, self._shape.rect)

    def set_position(self, position: Tuple[float, float]):
        self._shape.rect.center = position

    def get_position(self):
        return self._shape.rect.center

    def get_rect(self):
        return self._shape.rect

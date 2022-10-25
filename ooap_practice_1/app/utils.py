from typing import Tuple
import pygame
from enum import Enum

class ColorManager(Enum):
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

class HandlerActionStatus(Enum):
    NIL=0
    OK = 1
    BAD = 2

class HandlerAction:
    def __init__(self, lambda_):
        self._lambda = lambda_

    def process(self) -> HandlerActionStatus:
        return self._lambda()

class EventHandler:
    def __init__(self):
        self._actions = dict()

    def handle(self, event: pygame.event.Event, action : HandlerAction):
        if event in self._actions:
            return "BAD"
        self._actions[event] = action
        return "OK"

    def process(self, event: pygame.event.Event) -> HandlerActionStatus:
        if event not in self._actions:
            return HandlerActionStatus.NIL
        return self._actions[event]()


class WindowInfo:
    def __init__(self, fps: int, weight: int, heigh: int):
        self._fps = fps
        self._weight = weight
        self._heigh = heigh

    def get_fps(self):
        return self._fps

    def get_screen_size(self) -> Tuple[int, int]:
        return (self._weight, self._heigh)

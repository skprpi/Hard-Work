from typing import Tuple
import pygame
from enum import Enum
from abc import ABC, abstractmethod
from utils import ColorManager, WindowInfo
from random import randint
from math import sqrt
import time
import os


class SimpleView(ABC):
    def __init__(self, color: Tuple[int, int, int], shape: pygame.sprite.Sprite, window):
        self._color = color
        self._shape = shape
        self._window = window

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def get_center_position(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def set_center_position(self, position: Tuple[int, int]):
        pass

    @abstractmethod
    def rect(self) -> pygame.rect.Rect:
        pass


class RectangleView(SimpleView):
    def __init__(self, position: Tuple[int, int], width: int, heigh: int, color: Tuple[int, int, int], window):
        view = pygame.sprite.Sprite()
        view.rect = pygame.Rect(position[0], position[1], width, heigh)
        super().__init__(color, view, window)

    def draw(self):
        pygame.draw.rect(self._window, self._color, self._shape.rect)

    def get_center_position(self):
        return self._shape.rect.center

    def set_center_position(self, position: Tuple[int, int]):
        self._shape.rect.center = position

    def rect(self):
        return self._shape.rect


class Controller(ABC):
    @abstractmethod
    def get_next_position(self, position: Tuple[int, int], speed: int):
        pass


class KeyController(Controller):
    def get_next_position(self, position: Tuple[int, int], speed: int) -> Tuple[int, int]:
        presed_keys = pygame.key.get_pressed()
        X, Y = position
        X += (presed_keys[pygame.K_RIGHT] - presed_keys[pygame.K_LEFT]) * speed
        Y += (presed_keys[pygame.K_DOWN] - presed_keys[pygame.K_UP]) * speed
        return (X, Y)

class UnitClass(Enum):
    PLAYER = 0
    ZOOMBY = 1


class Unit(ABC):
    def __init__(self, unit_class: UnitClass, controller: Controller, view: SimpleView, start_speed: int):
        self._unit_class = unit_class
        self._controller = controller
        self._view = view
        self._speed = start_speed
        self.rect = self._view.rect()

    def process_collision(self, other):
        pass

    def __update_position(self):
        curr_position = self._view.get_center_position()
        new_position = self._controller.get_next_position(curr_position, self._speed)
        self._view.set_center_position(new_position)

    def draw(self):
        self.__update_position()
        self._view.draw()

    def position(self) -> Tuple[int, int]:
        return self.rect.center


class Player(Unit):
    def __init__(self, controller: Controller, view: SimpleView, start_speed: int):
        super().__init__(UnitClass.PLAYER, controller, view, start_speed)


# calculate next position according to target position (but update target position not each time)
class LazyTargetController(Controller):
    def __init__(self, target: Unit, target_update_position_time_ns: int):
        self._target_position = target._view.get_center_position()
        self._target = target
        self._timer_delta = target_update_position_time_ns
        self._start_time = time.time_ns()

    def get_next_position(self, position: Tuple[int, int], speed: int) -> Tuple[int, int]:
        if time.time_ns() - self._start_time > self._timer_delta:
            self._start_time = time.time_ns()
            self._target_position = self._target._view.get_center_position()
        X, Y = position
        X1, Y1 = self._target_position
        X += (1 if (int)(X1 >= X) else -1) * speed
        Y += (1 if (int)(Y1 >= Y) else -1) * speed
        return (X, Y)


# calculate next position according to target position
class TargetController(LazyTargetController):
    def __init__(self, target: Unit):
        super().__init__(target, 0)


class Zoombee(Unit):
    def __init__(self, controller: TargetController, view: SimpleView, start_speed: int):
        super().__init__(UnitClass.ZOOMBY, controller, view, start_speed)


class RandomPositionFactory:
    def __init__(self, player: Player, window_info: WindowInfo, min_enymy_dist: int):
        self._player = player
        self._window_info = window_info
        self._min_enymy_dist = min_enymy_dist

    def get_random_pos(self):
        while True:
            X, Y = self._player.position()
            X1, Y1 = randint(0, self._window_info._weight), randint(0, self._window_info._heigh)
            if sqrt(abs(X - X1) ** 2 + abs(Y - Y1) ** 2) > self._min_enymy_dist:
                return X1, Y1


def create_player(size, window):
    view = RectangleView((0, 0), size, size, ColorManager.RED.value, window)
    controller = KeyController()
    return Player(controller, view, 3)


class UnitsFactory:
    def __init__(self, player: Player, window, window_info: WindowInfo, unit_size):
        self._window = window
        self._unit_size = unit_size

        self._player = player

        self._pos_factory = RandomPositionFactory(self._player, window_info, 100)
        self.units = []

    def create_smart_zoombie(self):
        controller = TargetController(self._player)
        pos = self._pos_factory.get_random_pos()
        view = RectangleView(pos, self._unit_size, self._unit_size, ColorManager.BLUE.value, self._window)
        speed = randint(1, 2)
        return Zoombee(controller, view, speed)

    def create_zoombie(self):
        time_delta = randint(2000000000, 4000000000) # 1,5 - 3 sec
        controller = LazyTargetController(self._player, time_delta) # 1sec
        pos = self._pos_factory.get_random_pos()
        view = RectangleView(pos, self._unit_size, self._unit_size, ColorManager.GREEN.value, self._window)
        speed = randint(1, 4)
        return Zoombee(controller, view, speed)

    def create_sleeping_zoombie(self):
        controller = TargetController(self._player)
        pos = self._pos_factory.get_random_pos()
        view = RectangleView(pos, self._unit_size, self._unit_size, ColorManager.BLACK.value, self._window)
        return Zoombee(controller, view, 0)

    def create_random_unit(self):
        d = {
            "zombee" : self.create_zoombie,
            "smart_zombee" : self.create_smart_zoombie,
            "sleeping_zombee" : self.create_sleeping_zoombie,
        }
        lst = []
        for key in d:
            val = d[key]
            if os.getenv(key) == "on":
                lst.append(val)
        assert(len(lst))
        return lst[randint(0, len(lst) - 1)]()


class EnemyGroup:
    def __init__(self):
        self._units = []

    def add(self, unit: Unit):
        self._units.append(unit)

    def get_sprite_unit_group(self):
        return pygame.sprite.Group([el._view._shape for el in self._units])

    def draw_all(self):
        for el in self._units:
            el.draw()
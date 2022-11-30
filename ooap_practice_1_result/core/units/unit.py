from abc import ABC, abstractmethod
from core.units.state import UnitState


class Unit(ABC):
    def __init__(self, move_op, state: UnitState):
        self._state = state
        self._move_op = move_op

    def set_state(self, other: UnitState):
        self._state = other

    def get_position(self):
        return self._state._view.get_position()

    def draw(self):
        self._state.draw()

    def get_rect(self):
        return self._state.get_rect()

    def move(self, speed):
        self._state._view.set_position(self._move_op(self.get_position(), speed))

    def collide(self, other):
        return self.get_rect().collidepoint(other.get_position())

    @abstractmethod
    def process_collision(self, other_units: list):
        ...

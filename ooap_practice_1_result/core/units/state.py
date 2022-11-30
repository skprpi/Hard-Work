from abc import ABC, abstractmethod
from core.units.view import UnitView


class UnitState(ABC):
    def __init__(self, view: UnitView):
        self._view = view

    def get_rect(self):
        return self._view.get_rect()

    @abstractmethod
    def draw(self):
        ...


class AliveUnitState(UnitState):
    def __init__(self, view: UnitView):
        super().__init__(view)

    def draw(self):
        self._view.draw()


class DeadUnitState(UnitState):
    def __init__(self, view):
        super().__init__(view)

    def draw(self):
        ...

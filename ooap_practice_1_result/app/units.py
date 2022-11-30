import pygame
from typing import List, Tuple
from core.units.unit import Unit
from core.units.view import UnitView
from core.units.state import AliveUnitState, DeadUnitState


class Player(Unit):
    def __init__(self, move_op, view: UnitView):
        super().__init__(move_op, AliveUnitState(view))

    def process_collision(self, other: List[Unit]):
        # for el in other:
        for el in other:
            if self.collide(el):
                self.set_state(DeadUnitState(self._state._view))
        return self


class Zombee(Unit):
    def __init__(self, move_op, view: UnitView):
        super().__init__(move_op, AliveUnitState(view))

    def process_collision(self, other: List[Unit]):
        return self

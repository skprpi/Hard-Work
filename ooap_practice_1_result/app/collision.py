from typing import List
from core.units.unit import Unit
from copy import copy


def process_collisions(units: List[Unit]) -> List[Unit]:
    return [copy(units[i]).process_collision(units[:i] + units[i + 1:]) for i in range(len(units))]

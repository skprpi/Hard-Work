from abc import ABC, abstractmethod
from ast import List
import copy
from dataclasses import field
from enum import Enum
from random import randint


class CellState(Enum):
    Alive = 1
    Dead = 2


class Cell(ABC):
    def __init__(self):
        self.neighors = 0

    @abstractmethod
    def get_symbol(self):
        ...

    @abstractmethod
    def calc_neighors(self, neighbors: list):
        ...
    
    @abstractmethod
    def permute(self):
        ...


class EmptyCell(Cell):
    def __init__(self):
        super(Cell).__init__()

    def get_symbol(self):
        return ""

    def calc_neighors(self, neighbors: list):
        self.neighors = 0

    def permute(self):
        return EmptyCell()


class NotEmptyCell(Cell):
    def __init__(self):
        super(Cell).__init__()

    def calc_neighors(self, neighbors: list):
        assert(len(neighbors) == 8)
        self.neighors = 0
        for cell in neighbors:
            if isinstance(cell, AliveCell):
                self.neighors += 1

    def permute(self):
        if 2 <= self.neighors <= 3:
            return AliveCell()
        return DiedCell()


class AliveCell(NotEmptyCell):
    def __init__(self):
        super(NotEmptyCell).__init__()

    def get_symbol(self):
        return "#"


class DiedCell(NotEmptyCell):
    def __init__(self):
        super(Cell).__init__()

    def get_symbol(self):
        return " "


class NoPlaceException(BaseException): # Added exception
    pass

class Field:
    def __init__(self, size: int):
        last_idx = size + 1
        field_len = size + 2
        self.field = [[EmptyCell() if i == last_idx or j == last_idx or i * j == 0 else DiedCell()
            for i in range(field_len)] for j in range(field_len)]

    def __get_random_died_pos(self):
        all_died_cell_pos = self.get_all_state_pos(DiedCell)
        if len(all_died_cell_pos) == 0:
            raise NoPlaceException()
        pos = randint(0, len(all_died_cell_pos) - 1)
        return all_died_cell_pos[pos]

    def set_random_pos_state(self, state: Cell, n: int):
        for _ in range(n):
            x, y = self.__get_random_died_pos()
            self.field[x][y] = state

    def __str__(self):
        return "\n".join(["".join([self.field[i][j].get_symbol()
            for j in range(1, len(self.field) - 1)]) for i in range(1, len(self.field) - 1)])

    def __get_neib(self, x, y):
        len_ = len(self.field)
        assert(x != 0 and y != 0)
        assert(x < len_ and y < len_)
        return list(filter(lambda x: x is not None, [self.field[i][j] if i != x or j != y else None
            for i in range(x - 1, x + 2) for j in range(y - 1, y + 2)]))

    def next_state(self):
        for i in range(1, len(self.field) - 1):
            for j in range(1, len(self.field) - 1):
                neighbors = self.__get_neib(i, j)
                self.field[i][j].calc_neighors(neighbors)
        self.field = [[self.field[i][j].permute() for j in range(len(self.field))] for i in range(len(self.field))]

    def get_all_state_pos(self, state):
        return list(filter(lambda x: x is not None, [[i, j] if isinstance(self.field[i][j], state) else None
            for i in range(len(self.field)) for j in range(len(self.field))]))

    def get_state_count(self, state):
        return len(self.get_all_state_pos(state))


class FieldFactory:
    @staticmethod
    def build(string_format: str, rule_dict):
        lst_format = list(string_format.split('\n'))
        len_ = len(lst_format)
        f = Field(len_)
        for i in range(1, len_ + 1):
            for j in range(1, len_ + 1):
                f.field[i][j] = rule_dict[lst_format[i - 1][j - 1]]()
        return f


f = Field(10)
f.set_random_pos_state(AliveCell(), 20)
print(f)
f.next_state()
print(f)

from random import randint
from app import DiedCell, EmptyCell, Field, AliveCell, FieldFactory
import pytest


def test_alive_cell():
    for i in range(1, 30):
        f = Field(i)
        cnt = randint(0, i * i)
        f.set_random_pos_state(AliveCell(), cnt)
        assert(f.get_state_count(AliveCell) == cnt)


def test_empty_cell():
    for i in range(1, 40):
        size = i
        cnt_empty_cells = size + 2 + size + 2 + size + size
        f = Field(size)
        assert(f.get_state_count(EmptyCell) == cnt_empty_cells)


def test_initial_state():
    for i in range(1, 40):
        size = i
        cnt_empty_cells = size + 2 + size + 2 + size + size
        cnt_died_cells = size * size
        f = Field(size)
        assert(f.get_state_count(DiedCell) == cnt_died_cells)
        assert(f.get_state_count(EmptyCell) == cnt_empty_cells)



@pytest.mark.parametrize("state,next_state",
    [
        (
            [
                "  #",
                " # ",
                "#  ",
            ],
            [
                " # ",
                "###",
                " # ",
            ],
        ),
        (
            [
                "  #  ",
                " #   ",
                "# #  ",
                "#  # ",
                "#    ",
            ],
            [
                " #   ",
                "#### ",
                "# ## ",
                "# #  ",
                " #   ",
            ],
        ),
    ]
)
def test_state(state, next_state):
    f = FieldFactory.build("\n".join(state), {" ": DiedCell, "#": AliveCell})
    f.next_state()
    assert(str(f) == "\n".join(next_state))

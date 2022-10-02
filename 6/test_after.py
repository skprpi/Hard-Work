from random import randint
from app import DiedCell, EmptyCell, Field, AliveCell, FieldFactory, NoPlaceException
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


###################################################################################### after reading

def test_a_lot_of_random_pos():
    # до этого я тестировал только "хорошие" сценарии
    # тут добавлена проверка для "плохого" сценария
    f = Field(1)
    f.set_random_pos_state(AliveCell(), 1)
    cought_exception = False
    try:
        f.set_random_pos_state(AliveCell(), 1)
    except NoPlaceException as err:
        cought_exception = True
    assert(cought_exception)

def test_zero_field():
    # Еще один непротестированный крайний случай
    f = Field(0)
    cought_exception = False
    try:
        f.set_random_pos_state(AliveCell(), 1)
    except NoPlaceException as err:
        cought_exception = True
    assert(cought_exception)


def test_exact_set_field():
    # Добавляем строгости для тестов где смотрели кол-во свободных клеток
    f = Field(5)

    assert(f.get_state_count(DiedCell) == 5 * 5)

    for _ in range(2):
        f.field[2][2] = AliveCell()
        assert(f.get_state_count(AliveCell) == 1)
        assert(f.get_state_count(DiedCell) == 5 * 5 - 1)

    f.field[4][2] = AliveCell()
    assert(f.get_state_count(AliveCell) == 2)
    assert(f.get_state_count(DiedCell) == 5 * 5 - 2)

    f.field[2][4] = AliveCell()
    assert(f.get_state_count(AliveCell) == 3)
    assert(f.get_state_count(DiedCell) == 5 * 5 - 3)

    f.field[4][4] = AliveCell()
    assert(f.get_state_count(AliveCell) == 4)
    assert(f.get_state_count(DiedCell) == 5 * 5 - 4)

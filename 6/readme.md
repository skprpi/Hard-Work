# Отчет

## Задача 1

### Оригиналы

### После изменения

### Как вносились изменения

* Изначально добавился тест `test_boom_sell_creation` который проверять работу подкласса `BoomCell`. Для минимизации изменений
изначально проверяем, что есть возможности добавлять клетку указанного типа и добовляем класс минимально соответствующий данным требованиям

```
# test1.py

def test_btest_boom_sell_creationoom_sell():
    f = Field(5)
    f.set_random_pos_state(BoomCell(), 1)
    assert f.get_state_count(BoomCell) == 1
```

* Чтобы в будующем проверить специфическую часть логики в начале нужно научить конструировать правильное поле с данным состоянием.
Хорошо, что я сделал достаточно гибким интерфейс и это можно делать на лету без изменения основного кода. В итоге получим
следующий тест

```
# test1.py

def test_boom_cell_builder():
    # note: numeration from 1:1
    state = [
        "   o ",
        " #   ",
        "o #  ",
        "#  # ",
        "#    ",
    ]
    f = FieldFactory.build("\n".join(state), {" ": DiedCell, "#": AliveCell, "o": BoomCell})
    positions = f.get_all_state_pos(BoomCell)
    assert(len(positions) == 2)
    assert([1, 4] in positions)
    assert([3, 1] in positions)
```

* Данная клетка на следующем ходу должна уничтожать все живые клетки вокруг, поэтому добавим проверку на данную часть логики

```
# test1.py

def test_boom_effect():
    state = [
        "   o ",
        " #   ",
        "o #  ",
        "#  # ",
        "#    ",
    ]
    next_state = [
        "     ",
        "     ",
        "  ## ",
        "  #  ",
        " #   ",
    ]
    f = FieldFactory.build("\n".join(state), {" ": DiedCell, "#": AliveCell, "o": BoomCell})
    f.next_state()
    assert(str(f) == "\n".join(next_state))
```

### Итоги

## Задача 1

### Оригиналы

### После изменения
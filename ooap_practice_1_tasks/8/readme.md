# Отчет

```
UnitView - АТД
  запросы:
    * abstract get_position()
  команды:
    * abstract draw()
    * abstract set_position(x, y)
```

Описание: АТД осталось без изменения (все так же как и в прошлом отчете)

```
UnitState - Частично реализованный класс
    * __init__ (UnitView)
  команды:
    * abstract draw()
```

Описание: по сравнению с прошлой итерацией убал методы mpl `get_state` `change_state` т к странно что состояние может менять само себя хотя его задача только инкапсулировать логику отображения объекта

```
Unit - Частично реализованный класс
    * __init__ (move_func, state: UnitState)
  запросы:
    * impl get_state()
  команды:
    * impl change_state(other: UnitState)
    * abstract process()
```

Описание: `process` будет вызываться для каждого юнита на каждом Fram-e

```
UnitPairObserver
    * __init__(data: List[List[unit_type_1 : Unit, unit_type_2 : Unit, action : function<void(Unit, Unit)>]]])
  команды:
    * impl observe(units: List[Unit])
```

Описание: `observe` предполагается вызывать на каждой итерации, данная функция будет выполнять действия над полученными объектами исходя из их типа на основе функции полученной в конструкторе

## Иерархия


```
* UnitView  -- impl -> RectangleUnitView
* UnitState -- impl -> AliveUnitState, DeadUnitState
* Unit      -- impl -> ZombeeUnit, FastZombeeUnit, NoWalkingZombeeUnit, Player
* UnitPairObserver

```

Классы справа - наследники класса слева. Классы внизу содержат 1 или N эклкмпляром АТД вверху (затрагивается только 1 уровень т е `Unit` содержит `UnitState`, но не содержит `UnitView`)

Все классы имплементации наследуются только от родителя т е `ZombeeUnit`, `FastZombeeUnit`, `NoWalkingZombeeUnit` это все имплементации класса `Unit` (не стал переписывать эти классы т к их суть осталась той же)

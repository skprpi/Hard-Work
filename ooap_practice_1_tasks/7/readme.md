# Отчет

## UnitView кластер

### Классы

* UnitView - АТД
    * abstract draw
    * abstract get_position
    * abstract set_position

* RectangleUnitView:
    * impl draw
    * impl get_position
    * impl set_position

### Описание

Пока предполагается что все персонажи будут квадратными для простоты реализации графики и вычислений

## UnitState кластер

### Классы

* UnitState - АТД
    * __init__ (UnitView)
    * impl get_state
    * abstract change_state
    * abstract draw

* AliveUnitState:
    * impl change_state
    * impl draw

* DeadUnitState:
    * impl change_state
    * impl draw

### Описание

Предполагается налтичие 2-х общих состояний для всех персонажей - живой/не живой. При этом `UnitState` умеет работать с `UnitView`. Использовал композицию т к форма персонажа может меняться (в дальнейших обновлениях) в течении игры.

## Unit кластер

### Классы

* Unit - ATД
    * __init__ (move_func, UnitState)
    * impl get_state
    * impl change_state -> callable by observer
    * impl process -> (draw and move unit)

* ZombeeUnit, FastZombeeUnit, NoWalkingZombeeUnit, Player
    * имплементирует коретный тип за счет вызова конструктора с определенными параметрами в классе Unit

* UnitFactory:
    * get_random_unit
    * get_..._unit

## UnitObserver Кластер

* UnitPairObserver - АТД
    * __init__
    * abstract observe

* UnitPairCollisionObserver
    * __init__ (...)
    * impl observe(...)


### Описание:

`UnitPairCollisionObserver::__init__` - принимает массив (Utype1, Utype2, process_func(Utype1, Utype2)) - массив из тройки: 2 типа объектов которые нужно обрабатывать и функция которая обработает эти объекты
`UnitPairCollisionObserver::observe` - принимает массив всех `Unit` и обрабатывает всех юнитов по парно согласно их функции обработки


## Рефлексия

Система кластеров достаточно сильно поменялась в сравнении с первой имплементацией

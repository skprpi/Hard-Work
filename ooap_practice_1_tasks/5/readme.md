# Отчет

## Классы проетирования

### UnitFactory

* описание: Позволяет конструировать каких-либо юнитов по определенным правилам.

### CollisionObserver

* описание: Позволяет "наблюдать" за объектами и выполнять какие-либо действия при их столкновении (например переводить объект из состояния "Alive" -> "Dead")

### UnitState

* описание: Для каждого типа персонажей будет предполагаться отдельный АТД отвечающий за состояние объекта. Реализация подразумевает переходы между состояниями


### Рефлексия

При выполнении прошлого задания мне удалось избавиться от "хранения персонажей в друг друге" с целью обработки коллизий, мне казаласб придуманная схема достаточно хорошей. Некий класс Observer наблюдает за объектом и потом производит ад ним действия. Теперь кажется что можно не совержать множество каких-либо действий т к для каждого персонажа придется отдельно прописывать логику на каждую коллизию и кажется что происходит расползание логики по всей программе. АТД `UnitState` призван решить эту проблему. Он будет контролировать действия которые может выполнять персонаж находясь в том или ином состоянии, а `Observer` будет только переводить из одного состояния в другое (Тут будет разумно написать жизненный цикл для всех персонажей и возможно даже получится сделать универсальную машину состояний)

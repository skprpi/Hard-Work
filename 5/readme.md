# Пример 1

* Итоговый вариант: https://github.com/skprpi/Hard-Work/blob/main/5/example1.cpp

* Изначально для класса `Area` получились следующий комментарии:

```
// Ответственность: данный класс отвечает за выбор городов, которые должна посетить машина и подсчет
// времени, которое затратит машина добираясь из первого города в последний, а так же проставление штрафов
// в случае если данный путь невозможно пройти. Так же класс предоставляет ... [на этом моменте я понял что что-то не так]
```

* Тут может возникнуто вопрос: а почему тут есть слово `Ответственность`? Что ж, это была не очень удачная 
попытка формализации для оформления моих комментариев в дальнейшем. Т е хотелось бы иметь набор вопросов
отвечая на которые можно было бы получить комментарий приемлимого качества, а иногда даже хорошего и отличного.

### Небольшое отступление и анализ 

* `как назовешь корабль, так он и поплывет` - кажется именно это у меня и получилось. Когда я писал этот комментарий
то с каждым предложением понимал что что-то не то. Во первых, стало ясно что SOLID-ом тут и не пахнет. В прошлых
заданиях при работе с данным куском кода я выделял некоторые доп сущности, но за 5 минут написания данного комментария
я смог разделить его чуть на большее кол-во: `Calculator` - считает путь по предоставленному району,
`FineCalculator` - считает штраф, `Optimizer` - переставляет города разными способами для уменьшения штрафа и 
оптимизации пути.

## Как я изменил свой ответ после неудачного коммента

* Возможно, это очевидно, но написав правильный вопрос (который и был в задании) стало проще думать. И в итоге
получилось это:

```
// Как код вписывается в общую систему? 
// Данный класс рассчитывает маршрут по которому должна проехать 1 машина, для обеспечения
// наименьшего времени в пути всех машин в сумме и минимизации простоев, используя методы
// оптимизации.
```

### Анализ (Что стало лучше ???)

* теперь более понятен контекст. понятнее он стал т к добавилось фраза `для обеспечения наименьшего времени в пути всех машин в сумме` 
эта фраза не относится к текущему коду класса но подразумевает контекст использования
* Убралось описание внктренностей: описание что есть штрафы
* Из описания понятно для каких задачь может быть использован класс

#  Вывод по 1 заданию

* (ВЫВОД НЕ ПО ТЕМЕ) Важно письменно ответить на вопрос: `Какова ответственность класса?`. Конкретно для меня это важно сделать письменно
т.к. бумага не подкупна в отличае от моего мозга, который с радостью пропустит этот процесс анализа и сам себе
скажет что `у нас 1 ответственность, давай уже дальше поехали`. Когда смотришь на записи все становится чуть более
структурированно и проще оценить самого себя
* Писать комментарии трудно. Не скажу что у меня получился идельный комментарий, но даже на него пришлось потратить 5 - 10 минут + анализ (8 - 10 минут)
* Пока не придумал более формальные требования для написания комментриев, а вопрос `как этот код вписывается в общую систему` 
имеет большую не однозначность в ответе


## Задача 2

* Код с комментарием: https://github.com/skprpi/Hard-Work/blob/main/5/example2.java

* Сам комментарий

```
// Как этот код вписывется в систему?
// Данный класс позволяет симулировать работу нескольких лифтов. Класс "принимает заказы"
// от пассажиров и сам подбирает нужный лифт, для нужного этажа
```

### Анализ комментария

* Комментарий содержит верхнеуровневое описание функциональности класса
* Коммантарий не содержит подробного описания как именно мы что-то делаем
* Смотря на данный коментарий можно быстро понять место класса в системе и не тратить время на долгое выянения 
как класс встраивается в систему (Конечно если он не был написал 10 лет назад :) )

# Вывод по 2 заданию

* комментарий может сократить время разработки (при условии актуальности)
* комментарии могут помогать понимать логический дизайн системы 

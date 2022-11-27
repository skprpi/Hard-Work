# Классы-структуры данных

## Анализ

Чтобы понять понадобятся ли какие-либо классы с специфическими структурами данных нужно определить все типы операций, которые будут производиться

## Операции

* Проверка коллизий (проверка что один коллайдер касается другого - в моем случае это пересечение прямоугольников). В классическом случае проверка не столкнулся ли персонаж с вражеским юнитом

## Возможные операции

* Если карта будет достаточно большой, то игроку захочется видеть своего персонажа на карте и видить вражеских юнитов
* При расширении пула юнитов могут появится разные группы (дружественные, враги, нетральные) и обработка коллизий станет сложнее

## Структуры данных (классический сценарий)

* Для проверки на столкновение можно пользоваться обычным списком т к не предполагается в классическом сценарии добавлять разные классы юнитов. Есть только игрок и его враги -> сложность проверки на коллизию O(n)

## Структуры данных (расширенный сценарий)

* Для отображения миникарты может понадобиться quad-tree - таким образом можно будет отображать разное кол-во юнитов разным цветом например и мы избавимся от излишней детализации
* При наличии большого числа юнитов рахных групп будет обходится нам в O(n^2) - если у нас n разных групп и n юнитов т е в худшем случае квадратичная сложность. Можно так же использовать Quad-tree и обрабатывать коллизии только в определенном квадрате (а лучше H3 от Uber). Тут конечно придется еще обрабатывать и 2 ближайших квадрата - т к могут быть пограничне случаи, но это точно сможет убрать проверку лишних коллизий

## PositionTree (Quad-tree or S3 uber)

* getNeighor() - вернет ближайших соседей
* update(pos) - обновит дерево по позиции какого-либо персонажа
* Описание: может быть использовано как для миникарты так и для уменьшения числа юнитов которые нужно проверять на коллизии

## Вывод

С 80% вероятностью мне не понадобятся специфические структуры данных для реализации MVP, но проектировать струкуры я буду с учетом возможного расширения и обязательно напишу как-нибудь свою реализациию quad-tree - давно уже хочу это сделать но все руки не доходят :)
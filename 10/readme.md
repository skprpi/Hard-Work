# Отчет

## Пример 1

### Было

```
if (terminal_nodes.find(name) == terminal_nodes.end()) { // делаем поиск и одновременно проверяем какое-то условие
    return {};
}
```
### Стало
```
auto it = terminal_nodes.find(name);
if (it == terminal_nodes.end()) {
    return {};
}
```

## Пример 2

### Было

```
return parse(data)->first.get("server").get("adress").try_get("ip"); // парсинг и получение результата поля + неявная проверка нулевого указателя и возможно segmentation fault
```

### Стало

```
auto* json_serializable = parse(data);
if (!json_serializable) {
    throw BadJson();
}
auto adress = json_serializable->first.get("server").get("adress")

return adress.try_get("ip")
```

## Пример 3

### Было

```
if (black_list.count([this, data] { check_parseble(data); return parse(data);}()) > 0 ) { // вычисляем можно ли разпарсить строку + парсинг + проверка что данные получены от пользователя не из black list-a
    ....
}
```

### Стало

```
const bool parsable = check_parseble(data);
if (!parsable) {
    throw NotParsable();
}
auto serializable_data = parse(data);
if (black_list.count(serializable_data) > 0) {
    ...
}
```

## Пример 4

### Было

```
uint64_t time = in_time / 1000 + 2; // /1000 -> перевод из милисекунд в секунды, +2 -> допустимое отклонение
if (time < delta) {
    ....
}
```
### Стало

```
uint64_t time_sec = in_time_ms / 1000;
int epsilon = 2;
if (time - delta < epsilon) {
    ....
}
```

## Пример 5

### Было

```
int max3(int a, int b, int c) {
    return a > b ? (b > c ? a : (a > c ? a : c)) : (b > c ? b : c); // много сравнений
}
```

### Стало

```
int max3(int a, int b, int c) {
    std::vector<int> vec = {a, b, c};
    std::sort(vec.begin(), vec.end());
    return vec[vec.size() - 1];
}
```

# Отчет

## Запрет ошибочного поведения на уровне АТД


### Пример 1 (исходное состояние)

```
class UserSettings {

    ...

    bool active;
    bool privateMode;
}
```

### Пример 1 (исправленное состояние)

```
class UserMode {
    virtual bool active() = 0;
};

class PublicMode : public UserMode {
    bool active() override {
        ...
    }
};

class PrivateMode : public UserMode {
    bool active() override {
        ...
    }
};

class UserSetting {
    void setMode(std::shared_ptr<UserMode> mode) {
        ...
    }
};
```

### Описание 

Изначально было возможно состояние active = true и privateMode = true, а в privateMode не должна отображаться активность пользователся. Для решения данной проблемы был создан АТД `UserMode` который на уровне типов запрещает ошибочное состояние

### Пример 2 (исходное состояние)

```
class Parser {
public:
    static void parse(const std::string& str) {
        if (str.empty()) {
            throw ...
        }
        ...
    }
};
```

### Пример 2 (исправленное состояние)

```
class SuburlFactory {
public:
    class Suburl() {
    public:
        Suburl(const std::string& data) : data(data) {}

        std::string get() const {
            return data;
        }

    private:
        std::string data;
    }

    enum class Status {
        OK = 1,
        ERR = 2
    };

    struct CreateResult {
        Status status;
        std::optional<Suburl> suburl;
    };

    static CreateResult create(const std::string& suburl) {
        if (suburl.empty()) {
            return {Status.ERR, std::none};
        }
        ... // other cheks
        return {Status.OK, Suburl(suburl)};
    }
}

class UrlParser {
public:
    static void parse(const SuburlFactory::SubUrl& suburl) {
        ...
    }
};
```

### Описание 

Раньше парсеру призодилось проверять является ли строка пустой. Мы ввели данное ограничение через систему типов и теперь никакой junior не сможет сломать наш код :)

## Отказ от дефолных конструкторов

### Пример 1 (исходное состояние)

```
template <typename Node>
class LowercaseAlphabetParser {

    LowercaseAlphabetParser() = default;

    Node parse(const std::string& s) {
        for (auto ch: s) {
            if ('a' <= ch && ch <= 'z') {
                ...
            }
        }
    }
};
```

### Пример 1 (исправленное состояние)

```
class Validator {
public:
    virtual bool valid(char ch) = 0;

    void bool valid(std::string str) {
        for (auto ch: str) {
            if (!valid(ch)) {
                return false;
            }
        }
        return true;
    }
}

class AlphabetValidator : public Validator {

    AlphabetValidator() = default;

    bool valid(char ch) override {
        return 'a' <= ch && ch <= 'z';
    }
};


template <typename Node>
class Parser {
public:
    LowercaseAlphabetParser(std::shared_ptr<Validator> validator) : validator(validator) {}

    Node parse(const std::string& s) {
        if (!validator.valid(s)) {
            ...
        }
        ...
    }

private:
    std::shared_ptr<Validator> validator
};
```

### Описание 

Избавление от дефолтного конструктора позволила сделать парсер универсальным и теперь можно создавать любой валидатор и парсер будет с ним работать. P.S. пример взят из моего кода и чуть упрощен для лаконичности кода


### Пример 2 (исходное состояние)

```
class MonstorFactory:

    def __init__(self):
        pass

    @staticmethod
    def get_zombee(cls):
        return Zombee()


def play():
    ...
    zombee = []
    for i in range(user_setting_monsters_per_second):
        zombee.append(MonstorFactory.get_zombee())
    ...
```


### Пример 2 (исправленное состояние)

```
class MonstorFactory:

    def __init__(self, monsters_per_request):
        self.monsters_per_request = monsters_per_request

    def get_zombee(self):
        return [Zombee() for _ in range(self.monsters_per_request)]


def play():
    ...
    factory = MonstorFactory(user_setting_monsters_per_second)
    zombee = factory.get_zombee()
    ...
```

### Описание 

В данном примере мы смогли унести ответственность за генерацию нужного числа зомби (мы знаем что за игру это число не меняется) в класс-фабрику а не делать for в нескольких местах для генерации нужного числа зомби


## Избегание примитивных типов

### Пример 1 (исходное состояние)

```
def paly_alive_game(n, m):
    ...
    cells = [[0 for _ in range(m)] for _ in range(n)]
    ...
```

### Пример 1 (исправленное состояние)

```
# orig: https://github.com/skprpi/Hard-Work/blob/main/6/app1.py

class Field:
    def __init__(self, size: int):
        last_idx = size + 1
        field_len = size + 2
        self.field = [[EmptyCell() if i == last_idx or j == last_idx or i * j == 0 else DiedCell()
            for i in range(field_len)] for j in range(field_len)]

f = Field(10)
...
```

### Описание

Данный пример был написан мной в 6 занятии hard-work. В нем я использовал свои типы клеток: EmptyCell, AliveCell, DiedCell ... и таким образом явно задал какая клатка в каком состоянии находится - и это лучше чем использовать например int для условного обозначения 0 - мертв, 1 - жив. Так же используется тип Field который инкапсулирует двумерный массив, а пользователю нужно передать только 1 число - размер поля

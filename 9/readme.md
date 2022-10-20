# 1.1

## Исходное состояние

```
bool validUrl(const std::string &url) {
    std::set<char> alphabet = getUrlAlphabet();
    for (auto el: url) {
        if (alphabet.count(el) == 0) {
            return false;
        }
    }
    return true;
}

```
## Рефакторинг

```
// orig: https://github.com/skprpi/Messenger/blob/main/microservices/core/tests/fuzz/utils.h

bool validUrl(const std::string &url) {
    try {
        std::string copy_url(url);
        TargetResolver resolver;
        resolver.addUrlToTrie(std::move(copy_url), "FAKE", fake_endpoint_func);
    } catch (ParseException &) {
        return false;
    }
    return true;
}
```
## Описание

Пример функции взят из проекта который я пишу в свободное время - а именно из core библиотеке для социальной сети (функция взята из теста этой библиотеки фаззированием https://github.com/skprpi/Messenger/tree/main/microservices/core/tests/fuzz ). Писал код где-то неделю назад и еще подумал что валидация урла далжна быть сделана так, чтобы при изменении кода не менять тест. И пришел к схеме, которая есть в рефакторинге - пытаемся добавить url как это делается в коде и если получилось - то считаем это правильным. Но осознанно думать о том, что нужно убрать из проекта по возможности функции, которые есть только в тестах начну после выполнения пункта 1.1 :)

# 1.2

## Исходное состояние

```
def H():
    print('H')
    E()

def E():
    print('H')
    L()

def L():
    print('L')
    O()

def O():
    print('O')

if __name__ == '__main__':
    H()
```
## Рефакторинг

```
class State(Object):
    @abstractmethod
    def process():
        pass

    @abstractmethod
    def next_state():
        pass

class H(State):
    def process():
        print('H')

    # H -> E
    def next_state():
        return E()

class E(State):
    def process():
        print('E')

    # E -> L
    def next_state():
        return L()

class L(State):
    def process():
        print('L')

    # L -> O
    def next_state():
        return O()

class O(State):
    def process():
        print('O')

    # L -> O
    def next_state():
        return None


if __name__ == '__main__':
    state = H()
    while state:
        state.process()
        state = state.next_state()
```
## Описание

Тут приведен упращенный пример кода, который я недавно имплементировал, но не могу показать. Идея в следующем: Пусть у нас есть переходы из разных состояний 'H -> E -> L -> O'. В первом варианте использования логика была вынесена в сем метод и он вызывал другой метод и т д. Чтобы распутать цепочку нужно сделать не мало щелчков мышкой. Передалал все это в небольшую иерархию классов в которой есть абстрактный класс и классы наследники которые реализуют переходы в нужное состояние. Теперь наш код более прозрачен и его легче читать :)

# 1.3

## Исходное состояние

```
// https://github.com/skprpi/salesman-problem/blob/master/src/area.h

Функции для которых будет одинаковый рефакторинг

double reverse(const uint32_t idx1, const uint32_t idx2);
double safe_reverse(const uint32_t idx1, const uint32_t idx2);
double best_segment_insertion(uint32_t idx1, uint32_t idx2);
double range_parallel_swap(uint32_t select_idx1, uint32_t select_idx2, uint32_t insert_idx);
```
## Рефакторинг

```
struct InsertIdx {
    InsertIdx(int i, int j) : i(i), j(j) {
        assert(i < j);
        assert(i >= 0);
    }

    const int i;
    const int j;
};

double reverse(const InsertIdx idxes);
...

```
## Описание

В данных функциях не так много аргументов как моглобы быть (сложно просто найти у себя в коде много аргументов, давно перестал передавать их в большом кол-ве) но зато отлично демонстрирует принцип. И так, предположим что 2 аргумена уже много - самое верное решение создать объект имеющий поля равные переданным аргументам, но НЕ ВСЕМ! Тут нужно посмотреть на набор функций и понять где еще нужны эти параметры и можно будет их объединить в нейкий контекст, теперь нужно передавать меньшее число аргументов. И на этом кажется все, но не совсем... Я добавил в код немного ассертов и казалось бы зачем, а дело в том что эти ассерты есть везде где передаются эти индексы, поэтому убил сразу всех зайцев. И уменьшил число аргументов и уменьшил кол-во написанного кода в функциях

# 1.4

## Исходное состояние

```
// orig https://github.com/ImageMagick/ImageMagick/blob/main/MagickCore/profile.c

// profile.c
static MagickBooleanType SetsRGBImageProfile(Image *image,
  ExceptionInfo *exception);

и такая же 1 в 1 функция в моем хедере но не статическая

// my_header.h

Magick::MagickBooleanType SetsRGBImageProfile(MagickCore::Image *image, MagickCore::ExceptionInfo *exception);
```
## Рефакторинг

```
Казалось бы разумное решение - вынести в отдельный хедер и подключить в 2 местах и использовать..., но есть одно но (см Описание)
```
## Описание

Недавно работал с библиотекой https://github.com/ImageMagick/ImageMagick и нужно было переписать функцию которая вызывает функцию `SetsRGBImageProfile` для опитмизации работы. Сложность в рефакторинге данного куса кода в том, что функция - static а значит видна только в с файле + не вынесена в https://github.com/ImageMagick/ImageMagick/blob/main/MagickCore/profile.h соответствующий хедер где ей самое место, чтобы разработчики могли переписать часть функций под себя. И теперь получается следующая ситация: функция в библиотеке, которую переодически обновляют, и менять что-то внутри локально не вариант т к в следующем же обновлении все полетит, поэтому появляется наш локальный дубликат. Он обеспечит некую "стабильность". Самым лучшим решением будет попросить разработчиков добавить в h файл функцию :)


# 1.5

## Исходное состояние

```
std::string getUrlAlphabet {
    std::string alphabet = "";
    for (char ch = 'a', CH = 'A'; ch <= 'z'; ++ch, ++CH) {
        alphabet += ch;
        alphabet += CH;
    }
    for (char ch = '0'; ch <= '9'; ++ch) {
        alphabet += ch;
    }
    return alphabet + "/";
}

std::string createRandomUrl(const uint8_t *data, size_t size) {
    static const std::string alphabet = getUrlAlphabet();
    std::string url;
    for (int i = 0; i < size; ++i) {
        const uint8_t num = data[i];
        const size_t idx = num % alphabet.size();
        url += alphabet[idx];
    }
    return url;
}

std::string createRandomValidUrl(const uint8_t *data, size_t size) {
    if (size == 0) {
        return "";
    }
    static const std::string alphabet = getUrlAlphabetWithoutSlash().delete('/'); // Чрезмерный результат, сначала получили потом удалили
    ...
}

```
## Рефакторинг

```
// orig https://github.com/skprpi/Messenger/blob/main/microservices/core/tests/fuzz/utils.h

std::string getUrlAlphabetWithoutSlash() {
    std::string alphabet = "";
    for (char ch = 'a', CH = 'A'; ch <= 'z'; ++ch, ++CH) {
        alphabet += ch;
        alphabet += CH;
    }
    for (char ch = '0'; ch <= '9'; ++ch) {
        alphabet += ch;
    }
    return alphabet; // Теперь без / возвращаем
}

std::string createRandomUrl(const uint8_t *data, size_t size) {
    static const std::string alphabet = getUrlAlphabetWithoutSlash() + "/"; // Теперь плюсуем слеш тут
    std::string url;
    for (int i = 0; i < size; ++i) {
        const uint8_t num = data[i];
        const size_t idx = num % alphabet.size();
        url += alphabet[idx];
    }
    return url;
}

// postcondition: valid url
std::string createRandomValidUrl(const uint8_t *data, size_t size) {
    if (size == 0) {
        return "";
    }
    static const std::string alphabet = getUrlAlphabetWithoutSlash(); // Не нужно удалять
    ...
}
```
## Описание

Первая ситуация может показаться странной, но она действительно была в процессе разработке (точнее как только я увидел что "/" нужно доболять и убирть в разных местах сразу вынес в функцию, а в примере просто привел как это могло бы быть). Весь этот рассказ к тому, чтобы описать откуда появляются избыточные результаты: со временем функция начинает использоваться в нескольких местах и сложно сразу сделать ее универсальной (P.S. когда написал эти строчки вспонил Вашу сегодняшюю статью) и по этому приходится менять со временем. Честно говоря, мое решение сейчас тоже не идеал. Хотошо было бы сделать так:

```
std::string getUrlAlphabetWithoutSlash() {
    std::string alphabet = "";
    for (char ch = 'a', CH = 'A'; ch <= 'z'; ++ch, ++CH) {
        alphabet += ch;
        alphabet += CH;
    }
    for (char ch = '0'; ch <= '9'; ++ch) {
        alphabet += ch;
    }
    return alphabet; // Теперь без / возвращаем
}

std::string getUrlAlphabet {
    return getUrlAlphabetWithoutSlash() + "/";
}
```

Так лучше сделать потому что потом функция скорее всего будет переименована в `getUrlAlphabetWithoutSlash -> getUrlAlphabetWithoutSpecialSympols`, а функию `getUrlAlphabet` будет еще возврвщвть `_\-` и возможно другие символы.

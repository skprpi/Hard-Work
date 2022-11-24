# Отчет

## Пример 1

### Было

```
def validate(...):
    ...

def process_request(self, request):
    ...

def post(request):
    valid = validate_params(request.params)
    if not valid:
        raise ...
    return process_request(request)
```

### Стало

```
class SafeRequest:
    def valid_params(self, params):
        ...

    def __init__(self, request):
        if not valid_params(request):
            raise ...
        ...

def process_request(self, request: SafeRequest):
    ...

def post(request):
    return process_request(SafeRequest(request))
```

### Описание

В данном примере был изменен подход к ошибкам: мы не допускаем ошибочных состояний вместо того чтобы валидировать некие состояния и потом пропускать эти данные в другие функции. Проверка была вынесена на уровень типов - в питоне это может быть не всегда эффективно но в статически типизируемых языках это точно будет отличным решением

## Пример 2

### Было

```
def do_action():
    ...

def test_timeout(timeout): // unused variable
    start_time = time.now()

    do_action()

    assert time.now() - start_time <= 20000


def test_some():
    ...
    test_timeout(2000)
    ...

```

### Стало

```
def do_action():
    ...

def test_timeout(timeout):
    start_time = time.now()

    do_action()

    assert time.now() - start_time <= timeout // use variable


def test_some():
    ...
    timeout = 2000 // added var
    assert timeout == timeout // added assert
    test_timeout(timeout)
    ...

```

### Описание

Данный пример теcта встречался в моей практике - я често говоря потратил даже в районе 2 - 5 минут меняя таймаут и пытаясь запустить заново, а он все падал :) В данном примере в качесве "страховки от дурака" автор кода игнорировал параметр передаваемый в функцию и внутри использовал константное значение. Чтобы не вызывать недопонимание у разработчиков делаем чтобы функция работала ожидаемо и выносим проверку на верхний уровень `assert timeout == timeout`

## Пример 3

### Было

```
class Image:
    ...

    def changeProfile(icc_profile):
        ...
        if self.Colorspace() == icc_profile.Colorspace():
            return 0
        ...


def iccColorSpace(image, icc_profile):
    image.ImageModify()
    curr_profile = image.Profile()
    err = image.changeProfile(icc_profile)
    if err != 0:
        raise ...
    ...
```

### Стало

```
class Image:
    ...

    def changeProfile(icc_profile):
        ...
        // delete checking
        ...


def iccColorSpace(image, icc_profile):
    if image.Colorspace() == icc_profile.Colorspace(): // move checks
        return
    image.ImageModify()
    curr_profile = image.Profile()
    err = image.changeProfile(icc_profile)
    if err != 0:
        raise ...
    ...
```

### Описание

Пример был взят из одной из библиотек работы с изображениями с которыми мне пришлось разбираться. Пришлось потратить время чтобы понять что функция ничего не делает если профиль колорспейсы совпадают и профиль не применяется. P.S. в примере было уменьшино число функций, в библиотеке на много больше вложенность этих функций. В качесте исправления проверку на равенство колорспейсов стоит вынести в самую верхнеуровневую функцию вместо того чтобы проверять это в одном из других вложенных функций

## Пример 4

### Было

```
def makeScale(...): // library internal function
    ...


def scaleImage(image, size: str):
    res = list(size.split(':'))
    if len(res) != 2:
        raise BadSize()
    x, y = res
    if not number(x) || not number(y):
        raise BadSize()
    makeScale(...)


image = ...
image_size = input()
scaleImage(image_size)
```

### Стало

```
class Geometry: // created class for data validation
    def __init__(self, x: int, y: int):
        assert x > 0 && y > 0
        ...

// library internal function deleted


def scaleImage(image, size: Geometry):
    ... // do main logick


image = ...
image_size = Geometry(*list(map(int, input().split()))
scaleImage(image_size)
```

### Описание

В данном примере мы избавились от функции валидации размера картинки передаваемой в виде строки с помощью класса `Geometry` который допускает только состояния с шириной и высотой картинки больше 0. Таким образом мы сохраняем только валидные состояния на уровне типов

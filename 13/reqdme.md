# Отчет

## Пример 1

### Было

```
class Router:
    def __init__(self):
        pass

    def start_grpc(self):
        self.start_grpc = True
        ...

    def start_rest(self):
        self.start_rest = True
        ...

    def finish(self):
        if self.start_rest:
            ...
        else:
            # start grpc
            ...

def start_routing_with_log(routing):
    f = file.open('err.log', 'w')
    if routing.strategy == 'grpc':
        routing.start_grpc()
        f.write('Processed grpc')
    elif ns.name == 'rest':
        routing.start_rest()
        f.write(f'Process rest')
    routing.finish()
    f.close()
```

### Стало

```
class GRPCStrategy:
    def __init__(self):
        ...

    def get_name(self):
        return 'GRPC'

    def start(self):
        ...

    def __exit__(self):
        # finish logick
        ...


class RESTStrategy:
    def __init__(self):
        ...

    def get_name(self):
        return 'REST'

    def start(self):
        ...

    def __exit__(self):
        # finish logick
        ...


class Router:
    def __init__(self, strategy):
        self._strategy = strategy
        self._strategy.start()

    def name(self):
        return self._strategy.get_name()
    ...


def start_routing_with_log(route_strategy):
    with open('err.log', 'w') as f:
        router = Router(route_strategy)
        f.write(f'Processed {router.name()}')

```

### Описание

В результате рефакторинга было произведено разделение логики на захват и освобождения ресурса от работы над этим ресурсом с помощью `with` для файла и `__exit__` для Роутера. Была зменена управляющая конструкция `if - else`. Конструкция была заменена длагодаря выделению отдельной сущности `RouteStrategy` и обработка ушла внутрь клаждого класса а с наружи не осталось методов инициализации и освобождения - для этого стали использовать `__init__` и `__exit__`


## Пример 2


### Было

```
import requests


def MakeRequest(retry_count, url, timeout):
    for _ in range(retry_count):
        success = False
        try:
            response = requests.get(url, timeout=timeout)
        except requests.ConnectionError:
            print(f'Bad connection with url {url}')
        else:
            success = True
        finally:
            print(f'Finished process retry {_}')

        if success:
            print('Finished request')
            return response
    print('Finished request')
    return None
```

### Стало

```
import requests


class HTTPGetRequest:
    def __init__(self, url, timeout, retry_cnt = 1, params=None):
        self._url = url
        self._params = params
        self._retry_cnt = retry_cnt
        self._timeout = timeout

    def ___make_response(self):
        try:
            response = requests.get(self._url, timeout=self._timeout)
        except requests.ConnectionError:
            print(f'Bad connection with url {self._url}')
            return None
        return response

    def __len__(self):
        return self._retry_cnt

    def __getitem__(self, i):
        if i >= len(self):
            raise IndexError
        res = self.___make_response()
        print(f'Finished process retry {i}')
        return res

    def __enter__(self):
        return self

    def __exit__(self):
        print('Finished request')



def MakeRequest(retry_count, url, timeout):
    with HTTPGetRequest(url, retry_count) as request:
        for response in request:
            if response is not None:
                return response
    return None

```

### Описание

При рефакторинге была заменена управляющая конфтрукция `try-exept-else-finally` на `with`. Данный пример был взят из моего очень старого кода, рефакторинг так же был основан на примере `https://gist.github.com/Maecenas/5878ceee890a797ee6c9ad033a0ae0f1` . Для этого перехода были введены следующие методы `__enter__` `__exit__` - для работы с `with` и `__getitem__` `__len__` для работы с циклом. В результате получился код с разделенной логикой между выдилением и освобождением ресурсов и работы с этими ресурсами

# Отчет

## Призрачные состояния

```
MagickPrivate Cache ClonePixelCache(const Cache cache)
{
  CacheInfo
    *magick_restrict clone_info;

  const CacheInfo
    *magick_restrict cache_info;                              // Призрачное состояние

  assert(cache != NULL);
  cache_info=(const CacheInfo *) cache;
  assert(cache_info->signature == MagickCoreSignature);
  if (IsEventLogging() != MagickFalse)
    (void) LogMagickEvent(TraceEvent,GetMagickModule(),"%s",
      cache_info->filename);
  clone_info=(CacheInfo *) AcquirePixelCache(cache_info->number_threads);
  clone_info->virtual_pixel_method=cache_info->virtual_pixel_method;
  return((Cache ) clone_info);
}
```

Данная переменная является призрачным состоянием т к сузествует только как каст другой переменной из сигнатуры функции.

## Погрешности/неточности

### Пример 1

```
MagickExport void *AcquirePixelCachePixels(const Image *image,size_t *length,
  ExceptionInfo *exception)
{
  CacheInfo
    *magick_restrict cache_info;

  assert(image != (const Image *) NULL);
  assert(image->signature == MagickCoreSignature);
  assert(exception != (ExceptionInfo *) NULL);
  assert(exception->signature == MagickCoreSignature);
  assert(image->cache != (Cache) NULL);
  (void) exception;
  cache_info=(CacheInfo *) image->cache;
  assert(cache_info->signature == MagickCoreSignature);
  *length=0;
  if ((cache_info->type != MemoryCache) && (cache_info->type != MapCache))
    return((void *) NULL);
  *length=(size_t) cache_info->length;
  return(cache_info->pixels);
}
```

Для расширения границ в данной функции неодходимо не обрабатывать `NULL` указатели. Чтобы это сделать нужно ввести доп ограничения на систему типов - запрещающие нулевой указатель и тогда ограничения на данный метод будут отсутствовать в виде явныз `assert`. Для данной функции применяется допустимое ослабление, но при этом добавляются ограничения на дополнительные типы данных (например на `NotNULLPtr`)

Спецификация может выглядеть следующим образом

```
AcquirePixelCachePixels возвращает массив пикселей для изображения
```

### Пример 2

```
class Player:

    def __init__(self, ct=None):
        self.controller = None

    ...

    def set_controller(self, ct):
        self.controller = ct

    def move():
        if not self.controller:
            return self.position
        return self.controller(self.position)

    ...
```

```
# AbstractController предоставляет возможность перемещения персонажа
class AbstractController:
    ...

class Controller(AbstractController):
    ...

class EmptyController(AbstractController):
    ...

class Player:

    def __init__(self, ct: AbstractController):
        self.controller = None

    ...

    def set_controller(self, ct):
        self.controller = ct

    def move():
        return self.controller(self.position) // ослабили ограничение

    ...
```

В данном примере получилось ослабить функцию `move` за счет исправления системы типов. Раньше у нас был класс контроллера или None, теперь мы ожидаем только тип контроллера, но ввели доп тип `EmptyController` для обработки перемещения персонажей которые должны стоять.

## Интерфейс не проще реализации

```
template typename<T>
class AbstractNotNullPtr {
public:
    // принимает сырой ненулевой указатель
    AbstractNotNullPtr(T*) {
        ...
    }

    // возвращает ненулевой указатель
    // гарантирует атомарность в многопоточной среде
    // гарантирует что полученный указатель не станет nullptr пока существует хотя бы один объект AbstractNotNullPtr
    // ...
    virtual T* get() = 0;
}
```

```
class Allocator {
    ...
}

class Data {
    ...
}

template typename<T>
class AbstractNotNullPtr {
public:
    // принимает сырой ненулевой указатель
    AbstractNotNullPtr(Allocator, Data) { // изменили тип принимаемых данных
        ...
    }
}
```

В данном примере на интерфейс ложится достаточно много условий, а реализация будет выглядеть намного компактнее (за счет того, что в ЯП встроены часть гарантий описанных в интерфейсе). Во втором листенге так же приведен пример избавления от каких-либо проверок внутри конструктора за счет собственной алокации памяти, что гарантирует не нулевое значение указателя

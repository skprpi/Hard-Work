# Найденные ошибки:

* функция `length` не делает проверку что массив не пуст
* `std::pair<uint32_t, uint32_t> gen_random_idxes(uint32_t max_len)` -> `assert(idx1 <= idx2);`
* `std::pair<uint32_t, uint32_t> gen_random_idxes(uint32_t max_len)` -> `assert(max_len < city.size());`. Как оказалось
корнем ошибки был вызов `auto res = gen_random_idxes(max_len);` в функции `std::vector<uint32_t> gen_range_parallel_idx(uint32_t max_len)` - что в опрочем ожидаемо т к раньше тестировал на больших данных только или на маленьких в своих тестах но эту опцию не тестировал:)
* как оказалось пришлось добавть функцию `get_city_size` чтобы продолжить фазирование (раньше при написании проекта держал это условие в голове хотя от него зависят и другие компоненты)

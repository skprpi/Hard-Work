// оригинал: https://github.com/skprpi/Algorithms/blob/main/NP-problems/VRP/main.cpp
// Overview:
// Применил следующие приемы для рефакторинга
//  - ad-hoc полиморфизм (внутри цикла обрабатываем депо и магазин)
//  - убрал все else
//  - заменил if на тернарный оператор где это возможно
//  - вынес сложные условия в функцию shop_open
//  - замена if математическими функциями (используем функцию max)
//  - убраны многоуровневые условия


// Cyclomatic Complexity: 1
void set_default_state() { // общая логика с конструктором
    capacity_fine = 0;
    capacity = 0;
    time_fine = 0;
    time_in_road = 0;
    all_fine = 0;
    is_ok = true;
}

// Cyclomatic Complexity: 2
bool shop_open(const Shop& shop) {
    return time <= shop.close_time && time <= shop.open_time;
}

// Cyclomatic Complexity: 3
void visit_shop(const Shop& shop) { // данный метод заменяет логику с 21 - 30 строку и с 39 - 48 в исходном примере
    // постусловие: установлено время после посещения магазина и устанавливаем штраф если посетили закрытый магазин
    time_fine += !(time <= shop.close_time) ? time - shop.open_time : 0; // избавились от else во внешнем цикле а if 
        // заменили тернарным оператором
    time = shop_open(shop) ? shop.open_time + shop.service_time : time;
        // избавились от двух вложенных if через тернарный оператор + вынесли проверку условия в функцию
    time += shop.service_time; // во всех ветках условиях делаем это дейсвие значит можно
        // вынести общую логику (избавились от else во вложеннос цикле)
}


// из-за ad-hoc полиморфизма увеличилось до 5 без него было 3 (но тогда дублировалась логика после цикла)

// Cyclomatic Complexity: 5
// Cyclomatic Complexity before: 10
void update_time(int fine) {
    if (path.empty()) { // перенёс проверку раньше тобы не делать лишних действий если массив пуст
        return;
    }
    set_default_state(); // создание отдельной функции для
        // вынесения общей логики инициализации (как в конструкторе)
    long double time = find_dist(depo, path[0]);
    time_in_road = time;
    capacity = path[0].demand;
    visit_shop(path[0]); // было дублирование части кода до цикла и в цикле

    for (int i = 0; i < path.size(); i++) {
        bool last_iteration = static_cast<bool>(i == path.size());
        const auto& next_shop = last_iteration ? depo : path[i + 1];
        long double dist = find_dist(path[i], next_shop); // ad-hoc полиморфизм: теперь обрабатываем депо и магазин
            // т к find_dist перегружена на 2 разных типа
        time += dist;
        time_in_road += dist;
        if (last_iteration) {
            break;
        }
        visit_shop(next_shop); // вынесли общую логику в метод + избавились от условий в цикле вообще
        capacity += next_shop.demand;
    }

    time_fine = std::max(time - depo.close_time, 0); // заменяем if на выражение
    capacity_fine = std::max(capacity - max_capacity, 0); // заменяем if на выражение
    all_fine = time_fine + capacity_fine;
    is_ok = static_cast<bool>(all_fine == 0); // заменяем if на выражение
        // (добавляем каст чтобы было приятнее читать код)
    time_in_road += fine * (all_fine);
}

int main() {
    return 0;
}

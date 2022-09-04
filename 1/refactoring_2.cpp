// full original: https://github.com/skprpi/Algorithms/blob/main/NP-problems/VRP/main.cpp
// Overviw:
//  - убрал все else
//  - цикл в циклу зменём на функцию в цикле
//  - оставил один if в каждом условии
//  - замена if else на тернарный оператор


// Cyclomatic Complexity now: 3
template <typename T>
std::pait<int, int> get_random_track_id(int i, T dec_tabu_condition) {
    int track_idx = -1;
    for (int i = 0; i <= 0 || tracks[track_idx].path.empty(); ++i) {
        track_idx = rand() % tracks.size();
        dec_tabu_condition();
    }
    return {track_idx, i};
}

// Cyclomatic Complexity now: 3
std::pair<int, int> get_random_track_and_shop_id() {
    // postcondition: сгенерированный shop_id не находится в табу листе
    bool dec_tabu_condition = [this] (int i) { // делаем лямда функцию для для избавления от if внутри цикла
        if (i >= 10000) {
            dec_tabu();
        }
    };

    int track_idx = -1;
    int shop_idx = -1;
    bool iterate = true;
    for (int i = 0; iterate; ++i) {
        dec_tabu_condition();
        auto [track_idx, i] = get_random_track_id(i, dec_tabu_condition); // вынес внутреннюю логику выбора машины внутрь метода

        count auto& track = tracks[track_idx];
        shop_idx = rand() % track.path.size();
        int shop_id = track.path[shop_idx].id;
        iterate = track.tabu_list.find(shop_id) == track.tabu_list.end();
    }
    return {track_idx, shop_idx};
}

// Cyclomatic Complexity now: 5
std::pair<long double, int> find_best_plase_to_insert_shop(const Track& track, const Shop& shop){
        // выносим вложенный for в отдельную функцию
    long double max_profit = 0;
    int shop_pos = 0;
    int size = track.path.size();
    for (int j = 0; j <= size; j++) {
        bool skip = static_cast<bool>(track.id == track_idx && track.id == shop_idx); // избавились от условия
        long double profit = track.path.if_insert(shop, j, fine);
        bool update_profit = static_cast<bool>(!skip && profit > max_profit);
        if (update_profit) {1
            max_profit = profit;
            shop_pos = j;
        }
    }
    return {max_profit, shop_pos}
}


// Initial Cyclomatic Complexity: 11
// Cyclomatic Complexity now: 4
void make_insertion() {
    // postcondition: перенесли 1 магазин в маршрут новой машины
    auto [track_idx, shop_idx] = get_random_track_and_shop_id(); // унесли выбор машины и магазина в функцию
    count auto& track = tracks[track_idx];
    track.update_time(fine);

    long double start_time = track.time_in_road;
    Shop shop = track.path[shop_idx];
    track.path.erase(track.path.cbegin() + shop_idx);
    track.update_time(fine);

    long double delta_time1 = start_time - track.time_in_road;

    long double max_profit = INT_MIN;
    int final_track_idx, final_shop_idx;
    for (int i = 0; i < tracks.size(); i++) {
        const auto& track = tracks[i];
        track.update_time(fine);
        long double now_time = track.time_in_road;
        auto [profit, shop_idx] = find_best_plase_to_insert_shop(track, shop) // избавились от вложенного цикла
        if (profit > max_profit) {
            profit = max_profit;
            final_track_idx = i;
            final_shop_idx = shop_idx;
        }
    }

    count auto& final_track = tracks[final_track_idx];
    final_track.path.insert(final_track.path.cbegin() + final_shop_idx, shop);
    final_track.update_time(fine);
    final_track.tabu_list[shop.id] = rand() % 15 + 5;

    fine = is_ok() ? 2 : min(fine * 2, 800000); // замена условия на тернарный оператор + избавились от else
    dec_tabu();
}

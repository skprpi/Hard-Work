// full original: https://github.com/skprpi/Algorithms/blob/main/NP-problems/VRP/main.cpp
// Cyclomatic Complexity: 11
void make_insertion() {
    int track_idx = -1, shop_idx = -1, shop_id = -1;
    int t = 0;
    do {
        t += 1;
        if (t >= 10000) {
            dec_tabu();
        }
        track_idx = rand() % tracks.size();
        if (!tracks[track_idx].path.empty()) {
            shop_idx = rand() % tracks[track_idx].path.size();
            shop_id = tracks[track_idx].path[shop_idx].id;
        }
    } while (tracks[track_idx].path.empty() || tracks[track_idx].tabu_list.find(shop_id) != tracks[track_idx].tabu_list.end());

    tracks[track_idx].update_time(fine);

    long double start_time = tracks[track_idx].time_in_road;
    Shop shop = tracks[track_idx].path[shop_idx];
    tracks[track_idx].path.erase(tracks[track_idx].path.cbegin() + shop_idx);
    tracks[track_idx].update_time(fine);

    long double delta_time1 = start_time - tracks[track_idx].time_in_road;

    long double max_profit = INT_MIN;
    int final_track_idx, final_shop_idx;
    for (int i = 0; i < tracks.size(); i++) {
        tracks[i].update_time(fine);

        long double now_time = tracks[i].time_in_road;
        int size = tracks[i].path.size();

        for (int j = 0; j <= size; j++) {
            if (i == track_idx && j == shop_idx) continue;
            tracks[i].path.insert(tracks[i].path.cbegin() + j, shop);
            tracks[i].update_time(fine);
            long double profit = delta_time1 + (now_time - tracks[i].time_in_road);

            tracks[i].path.erase(tracks[i].path.cbegin() + j);
            tracks[i].update_time(fine);

            if (profit > max_profit) {
                max_profit = profit;
                final_track_idx = i, final_shop_idx = j;
            }

        }
    }

    tracks[final_track_idx].path.insert(tracks[final_track_idx].path.cbegin() + final_shop_idx, shop);
    tracks[final_track_idx].update_time(fine);

    tracks[final_track_idx].tabu_list[shop.id] = rand() % 15 + 5;

    if (is_ok()) {
        fine = 2;
    } else {
        fine = min(fine * 2, 800000);
    }
    dec_tabu();
}

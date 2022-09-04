// ----------------------------------------------
// Initial Cyclomatic Complexity: 10
// ----------------------------------------------

void update_time(int fine) {
    capacity_fine = 0;
    capacity = 0;
    time_fine = 0;
    time_in_road = 0;
    all_fine = 0;
    is_ok = true;

    if (path.empty()) {
        return;
    }

    long double time = find_dist(depo, path[0]);
    time_in_road = time;
    capacity = path[0].demand;

    if (time <= path[0].close_time) {
        if (time <= path[0].open_time) {
            time = path[0].open_time + path[0].service_time;
        } else {
            time += path[0].service_time;
        }
    } else {
        time_fine += time - path[0].open_time;
        time += path[0].service_time;
    }


    for (int i = 0; i < path.size() - 1; i++) {

        long double dist = find_dist(path[i], path[i + 1]);
        time += dist;
        time_in_road += dist;

        if (time <= path[i + 1].close_time) {
            if (time <= path[i + 1].open_time) {
                time = path[i + 1].open_time + path[i + 1].service_time;
            } else {
                time += path[i + 1].service_time;
            }
        } else {
            time_fine += time - path[i + 1].open_time;
            time += path[i + 1].service_time;
        }

        capacity += path[i + 1].demand;
    }

    long double dist_ = find_dist(depo, path[path.size() - 1]);
    time += dist_;
    time_in_road += dist_;

    if (time > depo.close_time) {
        time_fine += time - depo.close_time;
    }
    if (capacity > max_capacity)
        capacity_fine = capacity - max_capacity;
    all_fine = time_fine + capacity_fine;
    if (all_fine != 0) {
        is_ok = false;
    }

    time_in_road += fine * (all_fine);
}

// original: https://github.com/skprpi/salesman-problem/blob/master/src/area.h

#ifndef SRC_AREA_H
#define SRC_AREA_H

#include "city.h"
#include <algorithm>
#include <cassert>
#include <climits>
#include <iostream>
#include <random>
#include <vector>

class Area {
  // Как код вписывается в общую систему? 
  // Данный класс рассчитывает маршрут по которому должна проехать 1 машина, для обеспечения
  // наименьшего времени в пути всех машин в сумме и минимизации простоев, используя методы
  // оптимизации.

  public:
    explicit Area(const std::vector<City> &city) : city{city}, path_length_prefix(city.size())
    {
        cacl_path_length(0);
    }

    double length() const
    {
        return path_length_prefix[path_length_prefix.size() - 1];
    }

    double recalc_length()
    {
        cacl_path_length(0);
        return length();
    }

    std::pair<uint32_t, uint32_t> gen_random_idxes(uint32_t max_len)
    {
        assert(max_len < city.size());
        static std::random_device dev;
        static std::mt19937 rng(dev());
        std::uniform_int_distribution<std::mt19937::result_type> idx1_rnd(1, city.size() - 3);
        uint32_t idx1 = idx1_rnd(rng);
        uint32_t last_idx = city.size() - 2;
        std::uniform_int_distribution<std::mt19937::result_type> idx2_rnd(idx1, std::min(idx1 + max_len, last_idx));
        uint32_t idx2 = idx2_rnd(rng);
        if (idx1 > idx2) { // TODO: fuzzer found bug
            std::swap(idx1, idx2);
        }
        assert(idx1 <= idx2);
        return std::make_pair(idx1, idx2);
    }

    // The operation don't change order of the first and last city
    double reverse(const uint32_t idx1, const uint32_t idx2)
    {
        return reverse_segment(idx1, idx2, false);
    }

    // The operation don't change order of the first and last city
    double safe_reverse(const uint32_t idx1, const uint32_t idx2)
    {
        if (idx1 == 0 || idx2 == city.size() - 1) {
            std::cout << "Can't move first and last city" << std::endl;
            return length();
        }
        return reverse_segment(idx1, idx2, true);
    }

    // The operation don't change order of the first and last city
    double best_segment_insertion(uint32_t idx1, uint32_t idx2)
    {
        if (idx1 == 0 || idx2 == city.size() - 1) {
            std::cout << "Can't move first and last city idx1 = " << idx1 << "idx2 = " << idx2 << std::endl;
            return length();
        }
        if (idx1 > idx2) {
            std::swap(idx1, idx2);
        }
        double current_length = length();
        double new_length = UINT32_MAX;
        uint32_t insert_idx = 0;
        for (int i = 0; i < idx1 - 1; ++i) {
            double result = path_length_after_left_insertion(idx1, idx2, i);
            if (result < new_length) {
                new_length = result;
                insert_idx = i;
            }
        }
        for (int i = idx2 + 1; i < city.size() - 1; ++i) {
            double result = path_length_after_right_insertion(idx1, idx2, i);
            if (result < new_length) {
                new_length = result;
                insert_idx = i;
            }
        }

        if (new_length < current_length) {
            make_segment_insertion(idx1, idx2, insert_idx);
            cacl_path_length(std::min(idx1, insert_idx));
            assert(std::abs(new_length - length()) < 1e-6);
        }
        return length();
    }

    double perfect_segment_len_5(uint32_t idx)
    {
        assert(idx != 0);
        assert(idx < city.size() - 1);
        if (idx == city.size() - 2) {
            // permutation for 1 city
            return length();
        }
        static const uint32_t segment_length = 5;
        const uint32_t idx1 = idx;
        const uint32_t idx2 = std::min(static_cast<uint32_t>(city.size()) - 2, idx1 + segment_length);

        std::vector<City> best_permutation(city.begin() + idx1, city.begin() + idx2 + 1);
        double best_path_length = length();

        // sort by idx to do all permutations
        std::sort(city.begin() + idx1, city.begin() + idx2 + 1);
        // ignore first permutation
        do {
            double new_path_length = path_length_after_perfect_segment(idx1, idx2);
            if (new_path_length < best_path_length) {
                best_permutation = std::move(std::vector<City>(city.begin() + idx1, city.begin() + idx2 + 1));
                best_path_length = new_path_length;
            }
        } while (std::next_permutation(city.begin() + idx1, city.begin() + idx2 + 1));

        // set best
        for (int i = idx1, j = 0; i <= idx2; ++i, ++j) {
            city[i] = std::move(best_permutation[j]);
        }
        cacl_path_length(0);
        assert(std::abs(best_path_length - length()) < 1e-6);
        // std::cout << best_path_length << " " << length() << std::endl;
        return length();
    }

    double range_parallel_swap(uint32_t select_idx1, uint32_t select_idx2, uint32_t insert_idx)
    {
        assert(select_idx1 != 0);
        assert(select_idx1 < city.size() - 1);

        assert(select_idx2 != 0);
        assert(select_idx2 < city.size() - 1);

        assert(insert_idx != 0);
        assert(insert_idx < city.size() - 1);

        assert(select_idx1 <= select_idx2);
        assert(!(select_idx1 <= insert_idx && insert_idx <= select_idx2));

        for (int i = select_idx1, j = insert_idx; j != select_idx1 && i <= select_idx2 && j < city.size() - 1;
             ++i, ++j) {
            std::swap(city[i], city[j]);
        }
        cacl_path_length(std::min(select_idx1, insert_idx));
        return length();
    }

    std::vector<uint32_t> gen_range_parallel_idx(uint32_t max_len)
    {
        static bool before = true;
        static std::random_device dev;
        static std::mt19937 rng(dev());

        assert(max_len < city.size());
        auto res = gen_random_idxes(max_len); // error found by fuzzer
        std::vector<uint32_t> ans;

        if (before && res.first - 1 > 0) {
            std::uniform_int_distribution<std::mt19937::result_type> idx1_rnd(1, res.first - 1);
            ans = {res.first, res.second, static_cast<uint32_t>(idx1_rnd(rng))};
        } else if (!before && res.second) {
            std::uniform_int_distribution<std::mt19937::result_type> idx1_rnd(res.second + 1, city.size() - 2);
            ans = {res.first, res.second, static_cast<uint32_t>(idx1_rnd(rng))};
        } else {
            ans = {1, 2, 3};
        }
        before = !before;
        return ans;
    }

    void show_city_id()
    {
        for (int i = 0; i < city.size(); ++i) {
            std::cout << city[i].get_id() << " ";
        }
        std::cout << std::endl;
    }

    size_t get_city_size() const
    {
        return city.size();
    }

  private:
    double city_permutation_path_length(const uint32_t idx1, const uint32_t idx2)
    {
        double path_length = 0;
        for (int i = idx1 + 1; i <= idx2; ++i) {
            path_length += city[i] - city[i - 1];
        }
        return path_length;
    }

    double path_length_after_perfect_segment(const uint32_t idx1, const uint32_t idx2)
    {
        assert(idx1 != 0);
        assert(idx1 < idx2);
        assert(idx2 < city.size() - 1);
        assert(idx2 - idx1 < 8);

        double length_before = path_length_prefix[idx1 - 1];
        double path_length_after = path_length_prefix[city.size() - 1] - path_length_prefix[idx2 + 1];
        double new_city_path =
            city_permutation_path_length(idx1, idx2) + (city[idx1 - 1] - city[idx1]) + (city[idx2 + 1] - city[idx2]);
        return length_before + path_length_after + new_city_path;
    }

    double path_length_after_left_insertion(int32_t idx1, uint32_t idx2, const uint32_t insert_idx)
    {
        assert(idx1 <= idx2);
        assert(idx1 != 0);
        assert(idx2 < city.size() - 1);
        assert(insert_idx < city.size() - 1);

        assert(insert_idx < idx1 - 1); // if (insert_idx = idx1 - 1) -> same construction
        // insert_idx can be 0

        double result = 0;
        uint32_t last_idx = path_length_prefix.size() - 1;

        result += path_length_prefix[insert_idx] + (city[insert_idx] - city[idx1]);

        result += path_length_prefix[idx2] - path_length_prefix[idx1] + (city[idx2] - city[insert_idx + 1]);

        result += path_length_prefix[idx1 - 1] - path_length_prefix[insert_idx + 1] + (city[idx1 - 1] - city[idx2 + 1]);

        result += path_length_prefix[last_idx] - path_length_prefix[idx2 + 1];
        return result;
    }

    double path_length_after_right_insertion(int32_t idx1, uint32_t idx2, const uint32_t insert_idx)
    {
        assert(idx1 <= idx2);
        assert(idx1 != 0);
        assert(idx2 < city.size() - 1);
        assert(insert_idx < city.size() - 1);

        assert(insert_idx > idx2);
        // insert_idx can be 0

        double result = 0;
        uint32_t last_idx = path_length_prefix.size() - 1;

        result += path_length_prefix[idx1 - 1] + (city[idx1 - 1] - city[idx2 + 1]);

        result += path_length_prefix[insert_idx] - path_length_prefix[idx2 + 1] + (city[insert_idx] - city[idx1]);

        result += path_length_prefix[idx2] - path_length_prefix[idx1] + (city[idx2] - city[insert_idx + 1]);

        result += path_length_prefix[last_idx] - path_length_prefix[insert_idx + 1];
        return result;
    }

    void make_segment_insertion(int32_t idx1, uint32_t idx2, const uint32_t insert_idx)
    {
        std::vector<City> new_city;
        if (insert_idx < idx1) {
            new_city.insert(new_city.end(), city.begin(), city.begin() + insert_idx + 1);

            new_city.insert(new_city.end(), city.begin() + idx1, city.begin() + idx2 + 1);

            new_city.insert(new_city.end(), city.begin() + insert_idx + 1, city.begin() + idx1);

            new_city.insert(new_city.end(), city.begin() + idx2 + 1, city.end());
        } else if (insert_idx > idx2) {
            new_city.insert(new_city.end(), city.begin(), city.begin() + idx1);

            new_city.insert(new_city.end(), city.begin() + idx2 + 1, city.begin() + insert_idx + 1);

            new_city.insert(new_city.end(), city.begin() + idx1, city.begin() + idx2 + 1);

            new_city.insert(new_city.end(), city.begin() + insert_idx + 1, city.end());
        } else {
            assert(false);
        }
        city = std::move(new_city);
    }

    // return new length. Inp: [idx1, idx2]
    double reverse_segment(uint32_t idx1, uint32_t idx2, bool safe_mode)
    {
        if (idx1 > idx2) {
            std::swap(idx1, idx2);
        }
        if (idx1 == idx2) {
            return length();
        }
        assert(idx1 != 0);
        assert(idx2 < city.size() - 1);
        double now_length = length();
        double new_length = path_length_arter_reverse(idx1, idx2);

        if (new_length < now_length || !safe_mode) {
            // reverse
            for (uint32_t i = idx1, j = idx2; i < j; ++i, --j) {
                std::swap(city[i], city[j]);
            }
            // recalc prefix sum
            cacl_path_length(idx1);
            assert(std::abs(new_length - length()) < 1e-6);
        }
        return length();
    }

    double path_length_arter_reverse(const uint32_t idx1, const uint32_t idx2)
    {
        assert(idx1 != 0);
        assert(idx1 < idx2);
        assert(idx2 < city.size() - 1);
        double new_length = 0;

        new_length += path_length_prefix[idx1 - 1] + (city[idx2] - city[idx1 - 1]);
        double end_original_segment = path_length_prefix[path_length_prefix.size() - 1] - path_length_prefix[idx2 + 1];
        new_length += (city[idx2 + 1] - city[idx1]) + end_original_segment;

        // add reversed segment length
        new_length += path_length_prefix[idx2] - path_length_prefix[idx1];
        return new_length;
    }

    void cacl_path_length(uint32_t idx)
    {
        if (idx == 0) {
            path_length_prefix[0] = 0.0;
            path_length_prefix[1] = 0.0;
            idx = 1;
        }
        for (int i = idx; i < city.size(); ++i) {
            path_length_prefix[i] = path_length_prefix[i - 1] + (city[i] - city[i - 1]);
        }
    }

    std::vector<City> city;
    std::vector<double> path_length_prefix;
};

#endif // SRC_AREA_H

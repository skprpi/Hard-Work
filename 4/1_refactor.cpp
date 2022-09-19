class RandomGenerator {
public:

    // теперь мы не зависим от класса City
    // приняв максимальный индекс и макимальную разницу между индексами генерируем пару
    std::pair<uint32_t, uint32_t> gen_random_idxes(uint32_t max_idx, uint32_t max_idx_diff)
    {
        std::uniform_int_distribution<std::mt19937::result_type> idx1_rnd(1, max_idx - 3);
        uint32_t idx1 = idx1_rnd(rng);
        uint32_t last_idx = max_idx - 2;
        std::uniform_int_distribution<std::mt19937::result_type> idx2_rnd(idx1, std::min(idx1 + max_idx_diff, last_idx));
        uint32_t idx2 = idx2_rnd(rng);
        if (idx1 > idx2) { // TODO: fuzzer found bug
            std::swap(idx1, idx2);
        }
        assert(idx1 <= idx2);
        return std::make_pair(idx1, idx2);
    }

    // так же не зависим от класса City а просто генерируем нужные индексы
    std::vector<uint32_t> gen_range_parallel_idx(uint32_t max_idx, uint32_t max_len)
    {
        static bool before = true;
        auto res = gen_random_idxes(max_len); // error found by fuzzer
        std::vector<uint32_t> ans;

        if (before && res.first - 1 > 0) {
            std::uniform_int_distribution<std::mt19937::result_type> idx1_rnd(1, res.first - 1);
            ans = {res.first, res.second, static_cast<uint32_t>(idx1_rnd(rng))};
        } else if (!before && res.second) {
            std::uniform_int_distribution<std::mt19937::result_type> idx1_rnd(res.second + 1, max_idx - 2);
            ans = {res.first, res.second, static_cast<uint32_t>(idx1_rnd(rng))};
        } else {
            ans = {1, 2, 3};
        }
        before = !before;
        return ans;
    }

private:
    static std::random_device dev;
    static std::mt19937 rng(dev());
};

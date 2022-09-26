// orig: https://github.com/skprpi/java_lab5/blob/master/src/Lift.java

import java.util.ArrayList;

public class Lift extends Thread {
  // Как этот код вписывется в систему?
  // Данный класс позволяет симулировать работу нескольких лифтов. Класс "принимает заказы"
  // от пассажиров и сам подбирает нужный лифт, для нужного этажа

    static ArrayList<ArrayList<Integer>> floor = new ArrayList<>();

    static void make_init() {
        for (int i = 0; i < 9; i++) {
            floor.add(new ArrayList<Integer>());
        }
        floor.get(0).add(8);
    }

    static synchronized void add_to_floor(int rand_floor, int rand_next_floor) {
        floor.get(rand_floor).add(rand_next_floor);
    }

    static synchronized int get_from_floor(int i, int j) {
        return floor.get(i).get(j);
    }

    static synchronized int get_size(int i) {
        return floor.get(i).size();
    }

    static synchronized void remove_floor(int i, int j) {
        floor.get(i).remove(j);
    }

    int[] cnt_people_to_floor = new int[9];

    int now_floor = 0;

    int max_people_cnt = 9;

    int now_people_cnt = 0;

    boolean is_empty = true;

    boolean is_go_up = true;

    int lift_idx;

    public Lift(int idx) {
        lift_idx = idx;
    }

    public synchronized void get_people_from_floor() {
        ArrayList<Integer> delete_idx = new ArrayList<>();
        int size = get_size(now_floor);

        if (size == 0) return;

        for (int i = 0; i < size; i++) {
            int next_floor = 1;
            try {
                next_floor = get_from_floor(now_floor, i);
            } catch (IndexOutOfBoundsException e) {
                return;
            }
            if (is_empty) {
                cnt_people_to_floor[next_floor] += 1;

                is_go_up = next_floor > now_floor;
                is_empty = false;
                now_people_cnt = 1;
                delete_idx.add(i);
            } else {
                if (now_people_cnt + 1 <= max_people_cnt) {
                    if (is_go_up == next_floor > now_floor) {
                        cnt_people_to_floor[next_floor] += 1;
                        now_people_cnt += 1;
                        delete_idx.add(i);
                    }
                } else {
                    break;
                }
            }
        }
        for (int i = delete_idx.size() - 1; i >= 0; i--) {
            int del_pos = delete_idx.get(i);
            if (del_pos >= get_size(now_floor))
                continue;

            try {
                remove_floor(now_floor, del_pos);
            } catch (IndexOutOfBoundsException e) {
                return;
            }

        }
    }

    public synchronized void leave_people() {
        now_people_cnt -= cnt_people_to_floor[now_floor];
        cnt_people_to_floor[now_floor] = 0;
        is_empty = now_people_cnt == 0;
    }

    public synchronized void add_to_show() {
        ShowTower.lift_pos[lift_idx] = now_floor;
        ShowTower.cnt_people[lift_idx] = now_people_cnt;
        ShowTower.show();


        int rand_floor = 1;
        int rand_next_floor = 1;
        while (rand_floor == rand_next_floor) {
            rand_floor = (int)(Math.random() * 10000) % 9;
            rand_next_floor = (int)(Math.random() * 10000) % 9;
        }

        add_to_floor(rand_floor, rand_next_floor);
    }

    @Override
    public void run() {
        while (true) {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }



            leave_people();
            get_people_from_floor();
            if (!is_empty) {
                if (is_go_up) {
                    now_floor += 1;
                } else {
                    now_floor -= 1;
                }
            }
            add_to_show();
        }
    }
}

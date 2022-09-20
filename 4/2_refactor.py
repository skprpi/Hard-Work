class Person:
    def __init__(self, current_floor, next_floor):
        self.current_floor = current_floor
        self.next_floor = next_floor


class Lift:
    def __init__(self, cnt_floors, current_floor):
        self.state = LiftUp(cnt_floors, current_floor)

    def add_order(self, a, b, person):
        return self.state.add_order(a, b, person)

    def go_next(self):
        return self.state.go_next()


class LiftUp:
    def __init__(self, cnt_floors, current_floor):
        self.cnt_flors = cnt_floors
        self.current_floor = current_floor
        self.floor_take_person = dict()
        self.floor_out_person = dict()
        self.persons = []

    # заказываем лифт
    def add_order(self, a, b, person):
        if self.current_floor > a > b:
            self.floor_take_person[a].append(person)
            self.floor_out_person[b].append(person)
            return "ok"
        raise "Unvalliable to take a person"

    # лифт едет на следующий этаж
    def go_next(self):
        if self.current_floor in self.floor_take_person: # забираем кого нужно забрать
            self.persons += self.floor_take_person[self.current_floor]
        if self.current_floor in self.floor_out_person: # вызадили всех кого надо
            self.persons = list(set(self.persons).difference(set(self.floor_out_person[self.current_floor])))


class DownLift:
    pass
    # as a up lift


class LiftManager:
    def __init__(self, lifts: List[Lift]):
        self.lifts = lifts

    def manage(self, a, b, person):
        pass

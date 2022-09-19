class Person:

    def __init__(self, floor):
        self.floor = floor

    def put_button(self, lift):
        lift.add_order(self.floor)


class Lift:
    def __init__(self, cnt_floors):
        self.state = UpLift(cnt_floors, 1)
    
    def go_next(self):
        self.state = self.state.go_next()

    def add_order(self, n):
        self.state.add_order(n)

    def empty(self):
        self.state.empty()


class UpLift:
    def __init__(self, cnt_floors, current_floor):
        self.cnt_flors = cnt_floors
        self.current_floor = current_floor
        self.floor_person = dict()
        self.down_lift = DownLift()
        self.order_list = set()

    # заказываем лифт
    def add_order(self, n):
        if n >= self.cnt_flors:
            self.order_list.add(n)
            return
        self.down_lift.order_list.add(n)

    def empty(self):
        return len(self.persons) == 0

    # лифт едет на следующий этаж
    def go_next(self, avaliable_person):
        if self.current_floor in self.order_list: # забираем кого нужно забрать
            self.__add_person(avaliable_person)
            self.order_list.remove(self.current_floor) # убираем из очереди
        del self.floor_person[self.current_floor] # вызадили всех кого надо
        if self.cnt_flors == self.current_floor:
            return self.down_lift # начинаем опискаться
        self.current_floor += 1
        return self

    def __add_person(self, person):
        if person.floor >= self.current_floor:
            self.floor_person[person.floor].append(person)
            return
        self.down_lift.floor_person[person.floor].append(person)


class DownLift:
    # as a up lift
        

class LiftManager:

    def __init__(self, lifts: List[Lift])
        self.lifts = lifts

from agent import Agent
from Model import flight


class Task(flight.Flight):
    def __init__(self, number, park_p, passenger_p, arrive_time, update_time, flight_type):
        super().__init__(number, arrive_time, update_time, flight_type)
        if self.f_type == 1:
            self.p_pass = park_p
            self.p_end = passenger_p
        else:
            self.p_pass = passenger_p
            self.p_end = park_p
        self.state = 0
        # state=0 ==>not complete
        # state =1 ==>complete
        self.p_start = None
        self.task_t = 0
        self.task_s = None
        self.car = lambda: None
    # (x,y) "agent" ==>"task"

    def get_solve(self, car: Agent):
        # if not hasattr(self, 'car'):
        #     setattr(self, 'car', car)
        self.car = car
        # print(type(self.car))
        self.car.state = 1
        self.p_start = car.place
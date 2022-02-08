from agent import Agent_Base
from Model import flight


class Task(flight.Flight):
    def __init__(self, number, park_p, passenger_p, arrive_time, update_time, flight_type):
        super().__init__(number, arrive_time, update_time, flight_type)
        # the aircraft is going to arrive at the airport
        if self.f_type == 1:
            self.p_pass = park_p
            self.p_end = passenger_p
        # the aircraft is going to arrive at the airport
        else:
            self.p_pass = passenger_p
            self.p_end = park_p
        # state=0 ==>not completed
        # state =1 ==>completed
        self.state = 0

        self.car = lambda: None
        self.p_start = None
        # time and distance the car costs to complete the rask
        self.task_t = 0
        self.task_s = None

    def get_solve(self, car: Agent_Base):
        self.car = car
        # print(type(self.car))
        self.car.state = 1
        self.p_start = car.place
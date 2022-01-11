class Flight:
    def __init__(self, number, arrive_time, update_time, flight_type):
        self.number = number
        self.arrive_t = arrive_time
        self.update_t = update_time
        self.leave_t = None
        self.park_p = None
        self.passenger_p = None
        self.f_type = flight_type
class Flight:
    def __init__(self, number, scheduled_time, true_time, flight_type):
        # numerical order of the flight
        self.number = number
        # scheduled time to arrive the aircraft parking lot
        self.scheduled_arrive_t = scheduled_time
        # true time to arrive the aircraft parking lot
        self.true_arrive_t = true_time
        # time to leave the aircraft parking lot
        self.leave_t = None
        # the dispatched aircraft parking lot
        self.park_p = None
        # the dispatched passenger leave/arrive port of this flight
        self.passenger_p = None
        # the flight_type means the aircraft is going to leave from or arrive to the airport
        self.f_type = flight_type
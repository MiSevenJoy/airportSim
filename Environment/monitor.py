def check_and_return( ):
    # TODO: wait for writing
    '''
    if the car has finished its task at clock A
    the car can be redispatched at clock A+1,if it didn't get dispatched, it would return at clock A+2
    :param start_p1: parking lot1
    :param start_p2: parking lot2
    :return:
    '''
    for carAgent in self.bus_group:
        # if the car is not working and it isn't at the parking lot
        #
        if carAgent.state == 0 and carAgent.place != self.list_bus_p[0] and carAgent.place != self.list_bus_p[1]:
            if self.time - carAgent.t_end > 0:
                path = cal.calculation_2point(str(carAgent.place), str(random.choice(self.list_bus_p[0:2])),
                                              self.list_path)[0]
                carAgent.get_schedule(path)
                # print(path)
                carAgent.t_start = self.time + 1
                carAgent.state = 1
                self.bus_avai_group.remove(carAgent)
            else:
                self.bus_avai_group.add(carAgent)
                # print(carAgent.order)

    for carAgent in self.pc_group:
        # if the car is not working and it isn't at the parking lot
        #
        if carAgent.state == 0 and carAgent.place != self.list_bus_p[2] and carAgent.place != self.list_bus_p[3]:
            if self.time - carAgent.t_end > 0:
                path = cal.calculation_2point(str(carAgent.place), str(random.choice(self.list_bus_p[2:4])),
                                              self.list_path)[0]
                carAgent.get_schedule(path)
                # print(path)
                carAgent.t_start = self.time + 1
                carAgent.state = 1
                self.pc_avai_group.remove(carAgent)
            else:
                self.pc_avai_group.add(carAgent)
                # print(carAgent.order)
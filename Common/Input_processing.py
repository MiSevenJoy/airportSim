# create the bus and pc task for one flight
    def create_task(self, flt: flight.Flight):
        # flt.passenger_p, flt.park_p = self.dispatch_p()
        # create the bus and pc task for one flight
        if flt.park_p in self.list_far_p:
            locals()['bus_task' + str(flt.number)] = task.Task(flt.number, flt.park_p, flt.passenger_p, flt.arrive_t, flt.update_t, flt.f_type)
            self.bus_task_group.append(locals()['bus_task' + str(flt.number)])
            self.now_btg.append(locals()['bus_task' + str(flt.number)])
        locals()['pc_task' + str(flt.number)] = task.Task(flt.number, flt.park_p, self.package_center,
                                                     flt.arrive_t, flt.update_t, flt.f_type)
        self.pc_task_group.append(locals()['pc_task' + str(flt.number)])
        self.now_ptg.append(locals()['pc_task' + str(flt.number)])
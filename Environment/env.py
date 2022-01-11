import pygame          # 导入模块
from pygame.locals import *    # 导入pygame一些常用的函数和常量
from Decision import solution_random as solu_ran
from Model import agent, flight, task
from Common import parameter as para
from Map import excel_trans as ex_trans
import random
import copy
pygame.init()
info = pygame.font.SysFont('rachana', 25)


class Env:
    def __init__(self, bus_number, package_car_number, advance_time):
        # initial the screen & background image
        self.map_name = para.map_file
        self.list_far_p = None
        self.list_near_p = None
        self.list_path = None
        self.list_bus_p = None
        self.list_avai_p = None
        self.list_avai_passenger = None
        self.package_center = None
        self.map_info = None
        # task group only store uncompleted tasks
        self.bus_task_group = []
        self.pc_task_group = []
        self.now_btg = []
        self.now_ptg = []
        self.flight_group = []
        self.mark_group = pygame.sprite.Group()

        self.bus_group = pygame.sprite.Group()
        self.pc_group = pygame.sprite.Group()
        self.bus_avai_group = pygame.sprite.Group()
        self.pc_avai_group = pygame.sprite.Group()

        self.bus_n = bus_number
        self.pc_n = package_car_number
        self.flight_table = []
        self.time = 0
        self.advance_t = advance_time


    def init_env(self, flight_number, start_t, end_t):
        self.create_map()
        self.create_bus_pc()
        self.create_landmark()

        # put the flights into the environment
        self.create_flight(flight_number, start_t, end_t)

    # create the map and path for the environment
    def create_map(self):
        my_map = ex_trans.Excel_to_List(self.map_name, 'map')
        list_position = my_map.excel_to_pathlist()

        self.list_path = list_position[0]
        self.list_near_p = list_position[1]
        self.list_far_p = list_position[2]
        self.list_bus_p = list_position[3]
        self.list_avai_p = self.list_near_p + self.list_far_p
        self.package_center = list_position[4]
        self.list_avai_passenger = copy.deepcopy(self.list_near_p)

        self.map_info = ex_trans.Map_info(self.list_path)

    # create bus and pc for the environment
    def create_bus_pc(self):
        for i in range(self.bus_n):
            if i < int(len(self.bus_n)/2):
                locals()['bus' + str(i)] = agent.Agent(para.bus_img, self.list_bus_p[0], 0)
            else:
                locals()['bus' + str(i)] = agent.Agent(para.bus_img, self.list_bus_p[1], 0)
            self.bus_group.add(locals()['bus' + str(i)])
            self.bus_avai_group.add(locals()['bus' + str(i)])

        for j in range(self.pc_n):
            if j < int(len(self.bus_n)/2):
                locals()['pc' + str(j)] = agent.Agent(para.pc_img, self.list_bus_p[2], 1)
            else:
                locals()['pc' + str(j)] = agent.Agent(para.pc_img, self.list_bus_p[3], 1)
            self.pc_group.add(locals()['pc' + str(j)])
            self.pc_avai_group.add(locals()['pc' + str(j)])

    # put the land_mark on the screen to display
    def create_landmark(self):
        j = 0
        for j in range(len(self.list_near_p)):
            locals()['mark' + str(j)] = agent.Agent(para.passenger_near_img, self.list_near_p[j], 2)
            self.mark_group.add(locals()['mark' + str(j)])
        number = j
        for j in range(number + 1, number + len(self.list_far_p) + 1):
            locals()['mark' + str(j)] = agent.Agent(para.park_point_img, self.list_far_p[j - number - 1], 2)
            self.mark_group.add(locals()['mark' + str(j)])
        locals()['mark' + str(j + 1)] = agent.Agent(para.package_center_img, self.package_center, 2)
        self.mark_group.add(locals()['mark' + str(j + 1)])

    def env_render(self):
        '''
        :param agent_group: the shuffle and package car group
        :param mark_group: the land mark group
        :return:
        '''
        self.screen.blit(self.bg, (0, 0))  # update the background image
        self.create_landmark()
        # update the display of logos
        # self.set_landmark()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("end simulation...")
                pygame.quit()
                exit(0)
        # update the display of cars and landmarks
        self.mark_group.draw(self.screen)
        self.bus_group.update(self.time)
        self.pc_group.update(self.time)
        self.bus_group.draw(self.screen)
        self.pc_group.draw(self.screen)

        # update the screen
        pygame.display.update()
        info_fmt = info.render("time:"+str(self.time), True, (0, 0, 0))
        self.screen.blit(info_fmt, (0, 0))
        # 更新屏幕
        pygame.display.flip()
        pygame.time.delay(100)
        # environment render once, env time +1


    # create the bus and pc task for one flight
    def create_task(self, flt: flight.Flight):
        passenger_p = random.choice(self.list_avai_passenger)
        park_p = random.choice(self.list_avai_p)
        flt.passenger_p = passenger_p
        flt.park_p = park_p
        # choose and removed the chosen points
        self.list_avai_passenger.remove(passenger_p)
        self.list_avai_p.remove(park_p)
        # create the bus and pc task for one flight
        if park_p in self.list_far_p:
            locals()['bus_task' + str(flt.number)] = task.Task(flt.number, flt.park_p, flt.passenger_p, flt.arrive_t, flt.update_t, flt.f_type)
            self.bus_task_group.append(locals()['bus_task' + str(flt.number)])
            self.now_btg.append(locals()['bus_task' + str(flt.number)])
        locals()['pc_task' + str(flt.number)] = task.Task(flt.number, flt.park_p, self.package_center,
                                                     flt.arrive_t, flt.update_t, flt.f_type)
        self.pc_task_group.append(locals()['pc_task' + str(flt.number)])
        self.now_ptg.append(locals()['pc_task' + str(flt.number)])

    def create_flight(self, number, start_t, end_t):
        # create flight time table
        self.flight_table = [[] for i in range((start_t+1)*10, end_t*10-4)]
        for i in range(number):
            # 1==> in 0==>out
            flight_type = random.randint(0, 1)
            # schedule arrive time
            arrive_time = random.randint(start_t+1, end_t-1) * 10
            delay_time = random.randint(0, 5)
            # real arrive time
            # real_a_time = arrive_time + delay_time
            # make dispatching decision at update_time
            update_time = arrive_time+delay_time - self.advance_t
            locals()['flight' + str(i)] = flight.Flight(i, arrive_time, update_time, flight_type)
            self.flight_table[update_time].append(locals()['flight' + str(i)])
            # self.flight_group.append(locals()['flight' + str(i)])

    def step(self):
        # create task for every flight
        if len(self.flight_table[self.time]) > 0:
            # print(self.time)
            for flight in self.flight_table[self.time]:
                self.create_task(flight)
            # print(self.bus_task_group)
            # print(self.pc_task_group)
            for bus_task in self.now_btg:
                # RL algorithm makes decision on choosing car and time
                bus_task.get_solve(solu_ran.schedule_bus(self.bus_avai_group))
                # print(bus_task.p_start, bus_task.p_pass, bus_task.p_end)
                path = self.map_info.get_map_info(bus_task.p_start, bus_task.p_pass, bus_task.p_end)

                bus_task.car.get_schedule(path)
                bus_task.car.t_start = self.time + self.advance_t
                self.now_btg.remove(bus_task)

            for pc_task in self.now_ptg:
                pc_task.get_solve(solu_ran.schedule_pc(self.pc_avai_group))
                # print(pc_task.p_start, pc_task.p_pass, pc_task.p_end)
                path = self.map_info.get_map_info(pc_task.p_start, pc_task.p_pass, pc_task.p_end)
                # print(path)
                pc_task.car.get_schedule(path)
                pc_task.car.t_start = self.time + self.advance_t
                self.now_ptg.remove(pc_task)




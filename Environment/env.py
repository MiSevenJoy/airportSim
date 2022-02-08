import pygame          # 导入模块
from pygame.locals import *    # 导入pygame一些常用的函数和常量
from Controller import solution_random
from Model import agent, flight, task
from Common import parameter as para
from Map import excel_trans
import random
import copy
import operator
pygame.init()
info = pygame.font.SysFont('rachana', 25)


class Env_Base:
    def __init__(self, bus_number, package_car_number, advance_time):
        # attributes about environment map information
        self.list_far_p = None
        self.list_near_p = None
        self.list_path = None
        self.list_bus_p = None
        self.list_avai_p = None
        self.list_avai_passenger = None
        self.package_center = None
        self.map_info = None

        # uncompleted task group
        self.now_btg = []
        self.now_ptg = []

        self.bus_group = pygame.sprite.Group()
        self.pc_group = pygame.sprite.Group()
        self.bus_avai_group = pygame.sprite.Group()
        self.pc_avai_group = pygame.sprite.Group()

        self.bus_n = bus_number
        self.pc_n = package_car_number

        self.time = 0
        # the advanced time to make dispatching decision
        self.advance_t = advance_time
        # start_t to end_t : the time period to generate flights
        # self.start_t = start_t
        # self.end_t = end_t

    def init_env(self):

        self.create_map()
        # when the simulation needs visualization, the following two functions will be rewritten.
        self.create_bus_pc()

    # create the map and path for the environment
    def create_map(self):
        my_map = excel_trans.Excel_to_List(para.map_file, para.airport_name, para.rows, para.cols)
        list_position = my_map.excel_to_pathlist()

        self.list_path = list_position[0]
        self.list_near_p = list_position[1]
        self.list_far_p = list_position[2]
        self.list_bus_p = list_position[3]
        self.list_avai_p = self.list_near_p + self.list_far_p
        self.package_center = list_position[4]
        self.list_avai_passenger = copy.deepcopy(self.list_near_p)

        self.map_info = excel_trans.Map_info(list_position)

    # create bus and pc for the environment
    def create_bus_pc(self):
        for i in range(self.bus_n):
            if i < int(len(self.bus_n) / 2):
                locals()['bus' + str(i)] = agent.Agent_Base(self.list_bus_p[0], 0)
            else:
                locals()['bus' + str(i)] = agent.Agent_Base(self.list_bus_p[1], 0)
            self.bus_group.add(locals()['bus' + str(i)])
            self.bus_avai_group.add(locals()['bus' + str(i)])

        for j in range(self.pc_n):
            if j < int(len(self.bus_n) / 2):
                locals()['pc' + str(j)] = agent.Agent_Base(self.list_bus_p[2], 1)
            else:
                locals()['pc' + str(j)] = agent.Agent_Base(self.list_bus_p[3], 1)
            self.pc_group.add(locals()['pc' + str(j)])
            self.pc_avai_group.add(locals()['pc' + str(j)])

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
                bus_task.get_solve(solution_random.schedule_bus(self.bus_avai_group))
                # print(bus_task.p_start, bus_task.p_pass, bus_task.p_end)
                path = self.map_info.get_map_info(bus_task.p_start, bus_task.p_pass, bus_task.p_end)

                bus_task.car.get_schedule(path)
                bus_task.car.t_start = self.time + self.advance_t
                self.now_btg.remove(bus_task)

            for pc_task in self.now_ptg:
                pc_task.get_solve(solution_random.schedule_pc(self.pc_avai_group))
                # print(pc_task.p_start, pc_task.p_pass, pc_task.p_end)
                path = self.map_info.get_map_info(pc_task.p_start, pc_task.p_pass, pc_task.p_end)
                # print(path)
                pc_task.car.get_schedule(path)
                pc_task.car.t_start = self.time + self.advance_t
                self.now_ptg.remove(pc_task)



class Env(Env_Base):
    def __init__(self, bus_number, package_car_number, advance_time):
        super().__init__(bus_number, package_car_number, advance_time)
        # initial the screen & background image
        self.screen = pygame.display.set_mode((para.width, para.height))
        self.bg = pygame.image.load(para.bg_name)
        # put bg on the assigned point in the memory,the bg is not showed in this step
        self.screen.blit(self.bg, (0, 0))  # (x, y) is the left up location
        self.mark_group = pygame.sprite.Group()


    def init_env(self):

        self.create_map()
        # when the simulation needs visualization, the following two functions will be rewritten.
        self.create_bus_pc()
        self.create_landmark()

    # create bus and pc for the environment
    def create_bus_pc(self):
        for i in range(self.bus_n):
            if i < int(len(self.bus_n) / 2):
                locals()['bus' + str(i)] = agent.Agent(para.bus_img, self.list_bus_p[0], 0)
            else:
                locals()['bus' + str(i)] = agent.Agent(para.bus_img, self.list_bus_p[1], 0)
            self.bus_group.add(locals()['bus' + str(i)])
            self.bus_avai_group.add(locals()['bus' + str(i)])

        for j in range(self.pc_n):
            if j < int(len(self.bus_n) / 2):
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

    # update the visualization of the environment
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
        info_fmt = info.render("time:" + str(self.time), True, (0, 0, 0))
        self.screen.blit(info_fmt, (0, 0))
        # 更新屏幕
        pygame.display.flip()
        pygame.time.delay(100)
        # environment render once, env time +1
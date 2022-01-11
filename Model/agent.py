import pygame
import numpy as np

# should in common
from Common import parameter as scen


class Agent(pygame.sprite.Sprite):
    def __init__(self, image_name, place_list, sort):
        super().__init__()
        # 加载图像
        self.image = pygame.image.load(image_name)
        # 设置尺寸
        self.rect = self.image.get_rect()
        self.place = place_list
        # the way of display :topleft
        # also the initial position
        self.rect.topleft = [place_list[1]*scen.pixel_y, place_list[0]*scen.pixel_x]
        # # the place of agent
        # self.place = place
        # state = 0 ==> free
        # state = 1 ==> scheduled but not working
        # state = 2 ==> scheduled and working
        self.state = 0
        self.t_start = -1
        self.t_end = -1

        # sort = 0 ==> Shuttle car
        # sort = 1 ==> Package car
        # sort = 2 ==> landmark
        self.sort = sort

        self.schedule = None
        self.schedule_length = None
        self.last_p = None
        # the agent's order in the whole schedule
        self.order = 0
        # the pixel of each grid

    # get the position of agent
    def get_place(self):
        return self.place

    def get_schedule(self, list_schedule):
        self.last_p = list_schedule[len(list_schedule) - 1]
        self.schedule = np.array(list_schedule)
        #print(self.schedule)
        self.schedule_length = len(list_schedule)
        #print(self.schedule_length)

    # only when the agent is busy,it moves,when it finished one task, the state will be changed back to 0
    # when the car is free ,it has no schedule path
    def update(self, time, *args):
        # if self.state == 1 and self.work_state == 1:
        if self.t_start == time:
            self.state = 2
        if self.state == 2:
            d_move = self.schedule[self.order+1] - self.schedule[self.order]
            # print(d_move)
            self.place = self.schedule[self.order+1].tolist()
            self.rect.x += d_move[1] * scen.pixel_y
            self.rect.y += d_move[0] * scen.pixel_x
            # self.change_rect(d_move)
            self.order += 1
            if self.place == self.last_p:
                self.state = 0
                self.t_end = time
                self.t_start = -1
                self.order = 0

import pygame
import numpy as np

# should in common
from Common import parameter as para


# basic agent class statement without visualization
class Agent_Base(pygame.sprite.Sprite):
    def __init__(self, place, sort):
        super().__init__()
        self.place = place
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

        self.schedule = []
        self.schedule_length = None
        self.last_p = None
        # the agent's order in the whole schedule
        self.order = 0

    # get the position of agent
    def get_place(self):
        return self.place
    def reset(self):
        self.state = 0
        self.t_start = -1
        self.order = 0
        self.schedule = []

    def get_schedule(self, list_schedule):
        self.schedule_length = len(list_schedule)
        self.last_p = list_schedule[self.schedule_length - 1]
        self.schedule = np.array(list_schedule)

    def update(self, time, *args):
        # time : the system clock
        # t_start : the scheduled time to start to work
        if self.t_start == time:
            self.state = 2
        if self.state == 2:
            self.place = self.schedule[self.order+1].tolist()
            self.order += 1
            if self.place == self.last_p:
                self.reset()
                self.t_end = time

class Agent(Agent_Base):
    def __init__(self, image_name, place, sort):
        super().__init__(place, sort)
        # 加载图像
        self.image = pygame.image.load(image_name)
        # 设置尺寸
        self.rect = self.image.get_rect()
        # the way of display :topleft
        # also the initial position
        self.rect.topleft = [place[1] * para.pixel_y, place[0] * para.pixel_x]

    def update(self, time, *args):
        if self.t_start == time:
            self.state = 2
        if self.state == 2:
            d_move = self.schedule[self.order+1] - self.schedule[self.order]
            # print(d_move)
            self.place = self.schedule[self.order+1].tolist()
            self.rect.x += d_move[1] * para.pixel_y
            self.rect.y += d_move[0] * para.pixel_x
            # self.change_rect(d_move)
            self.order += 1
            if self.place == self.last_p:
                self.reset()
                self.t_end = time
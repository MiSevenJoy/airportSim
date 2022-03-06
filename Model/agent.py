import pygame
import numpy as np

# should in common
from Common import parameter as para


# basic agent class statement without visualization
class Agent_Base(pygame.sprite.Sprite):
    def __init__(self, name, place):
        super().__init__()
        self.name = name
        self.place = place
        # state = 0 ==> free
        # state = 1 ==> scheduled and working
        # state = 2 ==> reached the end
        self.state = 0
        self.t_end = -1
        self.last_p = None
        # the agent's order in the whole schedule

    def __repr__(self):
        return self.name+str(self.place)

    # get the position of agent
    @ property
    def get_place(self):
        return self.place

    def get_dispatch(self, t_end, p_end):
        self.t_end = t_end
        self.state = 1
        self.last_p = p_end
        # print('arrive at clock :' + str(self.t_end))

    def update(self, time, *args):
        # time : the system clock
        # t_start : the scheduled time to start to work
        if self.state == 1 and time == self.t_end:
            self.state = 2
            self.place = self.last_p


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
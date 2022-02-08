import random
import pygame
from task import *


def schedule_bus(bus_avai_group: pygame.sprite.Group):
    if len(bus_avai_group.sprites()) == 0:
        print('no available bus')
        return 0
    while True:
        bus = random.choice(bus_avai_group.sprites())
        if bus.state == 0:
            bus_avai_group.remove(bus)
            return bus


def schedule_pc(pc_avai_group: pygame.sprite.Group):
    if len(pc_avai_group.sprites()) == 0:
        print('no available package car')
        return 0
    while True:
        pc = random.choice(pc_avai_group.sprites())
        if pc.state == 0:
            pc_avai_group.remove(pc)
            return pc


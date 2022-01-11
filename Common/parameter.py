import numpy as np
import pygame
pixel_x = 31
pixel_y = 31

# picture location
package_center_img = '/home/lab/yue/PycharmProjects/simulation/logo/package_center.png'
park_point_img = '/home/lab/yue/PycharmProjects/simulation/logo/plane_point.png'
bus_img = '/home/lab/yue/PycharmProjects/simulation/logo/bus.png'
pc_img = '/home/lab/yue/PycharmProjects/simulation/logo/package_car.png'
passenger_near_img = '/home/lab/yue/PycharmProjects/simulation/logo/passenger_near.png'
map_file = '/home/lab/yue/PycharmProjects/simulation/airport_map.xls'
airport_name = 'baoan_airport'
map_info_file = '/home/lab/yue/PycharmProjects/simulation/airport_map.xls'
info = pygame.font.SysFont('rachana', 25)

# names of the path colors
YELLOW = np.array([255,255,0],dtype=int)
WHITE = np.array([255,255,255],dtype=int)
CYAN = np.array([0,255,255],dtype=int)
GREEN = np.array([0,0,255],dtype=int)
PURPLE = np.array([255,0,255],dtype=int)
RED = np.array([255,0,0],dtype=int)





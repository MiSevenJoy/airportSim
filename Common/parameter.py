import numpy as np
import pygame
# the unit length of agents' movement
pixel_x = 31
pixel_y = 31
# the rows and cols of the 'map_file'
rows = 32
cols = 22

# parameter to measure the airport's capacity
n_parking_lot = 40
n_passenger_lot = 24
n_flight = 20

# the range of acceptable delay time(min)
delay_t = 10
advance_time = 15
# picture location
package_center_img = '/home/lab/yue/PycharmProjects/simulation/logo/package_center.png'
park_point_img = '/home/lab/yue/PycharmProjects/simulation/logo/plane_point.png'
bus_img = '/home/lab/yue/PycharmProjects/simulation/logo/bus.png'
pc_img = '/home/lab/yue/PycharmProjects/simulation/logo/package_car.png'
passenger_near_img = '/home/lab/yue/PycharmProjects/simulation/logo/passenger_near.png'
map_file = '/home/joy/projects/airportSim/Common/Maps/airport_map.xls'
airport_name = 'baoan_airport'
map_info_file = '/Common/Maps/airport_map_info.xls'
path_file = '/home/joy/projects/airportSim/Common/Maps/path.txt'
original_flight_data = '/home/joy/projects/airportSim/Common/Input_data/original_flight_data.xlsx'
flight_data = '/home/joy/projects/airportSim/Common/Input_data/flight_data.xlsx'
task_data = '/home/joy/projects/airportSim/Common/Input_data/task_data.xlsx'
sheet_name = '2022_2_15'
# info = pygame.font.SysFont('rachana', 25)

# names of the colors
YELLOW = np.array([255,255,0],dtype=int)
WHITE = np.array([255,255,255],dtype=int)
CYAN = np.array([0,255,255],dtype=int)
GREEN = np.array([0,255,0],dtype=int)
PURPLE = np.array([255,0,255],dtype=int)
RED = np.array([255,0,0],dtype=int)





from Map.Path_Calculation import Calculation
import xlrd
import xlwt
from xlutils.copy import copy as xl_copy
# the index of xls starts from 1 when using openpyxl
from Common import parameter as para
import numpy as np
import os

'''
functions needed to be achieved in the file:
  1.read the map excel's colors as the path information
  2.background image generation
  3.preparation for the (least path length calculation)
'''

class Excel_to_List:

    def __init__(self, file_name, sheet_name, rows, cols):
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.book = None
        self.xf_list = None
        self.colour_map = None
        self.s = None
        self.rows = rows
        self.cols = cols

    # open the excel file
    def open_excel(self):
        try:
            self.book = xlrd.open_workbook(self.file_name, formatting_info=True)
        except Exception:
            print(u'useless file path')
        self.s = self.book.sheet_by_name(self.sheet_name)
        self.xf_list = self.book.xf_list
        self.colour_map = self.book.colour_map

    def get_cell_color(self, cell):
        xf_index = cell.xf_index
        xf_style = self.xf_list[xf_index]
        xf_background = xf_style.background
        pattern_colour_index = xf_background.pattern_colour_index
        pattern_colour = self.colour_map[pattern_colour_index]
        return np.array(pattern_colour, dtype = int)

    # get the excel file data
    def excel_to_pathlist(self):
        self.open_excel()
        # path cell : yellow
        # obstacle cell : white
        # nearby apron : green
        # far apron: cyan
        # parking lot: purple
        # package center: red
        list_path = []
        list_near_p =[]
        list_far_p =[]
        list_bus_p =[]
        package_center = []
        # index starts from 0
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                cell = self.s.cell(i, j)
                color = self.get_cell_color(cell)
                if not ((color == para.WHITE).all()):
                    list_path.append([i, j])
                    if (color == para.GREEN).all():
                        list_near_p.append([i, j])
                    elif (color == para.CYAN).all():
                        list_far_p.append([i, j])
                    elif (color == para.PURPLE).all():
                        list_bus_p.append([i, j])
                    elif(color == para.RED).all():
                        package_center.append([i, j])
        f = open(para.path_file, "w")
        f.writelines(str(list_path)+'\n')
        f.writelines(str(list_near_p)+'\n')
        f.writelines(str(list_far_p) + '\n')
        f.writelines(str(list_bus_p) + '\n')
        f.writelines(str(package_center) + '\n')
        f.close()
        # return list_path, list_near_p, list_far_p, list_bus_p, package_center

    def excel_array(self):
        self.open_excel()
        rows = self.s.nrows  # 总行数
        cols = self.s.ncols  # total columns
        array_map = np.empty((rows, cols))
        for i in range(0, rows):
            for j in range(0, cols):
                array_map[i][j] = self.s.cell_value(i, j)

        #print(array_map)
        return array_map

# directly get the path and distance of scheduling route
class Map_info:
    def __init__(self, path_list):
        # get all destination that shuffle bus or luggage van may go to
        self.path_list = eval(path_list[0])
        self.destination_list = eval(path_list[1])+eval(path_list[2])+eval(path_list[3])+eval(path_list[4])
        # check whether the map-information excel file has generated

        if os.path.exists(para.map_info_file):
            self.book = xlrd.open_workbook(para.map_info_file)
            self.sheet_path = self.book.sheet_by_index(0)
            self.sheet_distance = self.book.sheet_by_index(1)
        else:
            self.book = None
            self.sheet_path = None
            self.sheet_distance = None
            self.count_map_info()


    def count_map_info(self):
        # format translation:translate the excel to path list
        # Trans = Excel_to_List(para.map_file, para.airport_name)
        # path_list = Trans.excel_to_pathlist()

        Calcu = Calculation(self.path_list)
        # self.book = xlwt.Workbook()
        self.book = xlrd.open_workbook(para.map_info_file)
        # wb = xl_copy(self.book)
        self.sheet_path = self.book.add_sheet(para.airport_name + ' path')
        # self.sheet_path = self.book.sheet_by_index(0)
        self.sheet_distance = self.book.add_sheet(para.airport_name + 'distance')
        total_number = len(self.destination_list)
        # count the all distance between two points by traversing
        for i in range(total_number):
            for j in range(i, total_number):
                if i == j:
                    self.sheet_path.write(i, j, label = None)
                    self.sheet_distance.write(i, j, label = 0)
                else:
                    path, distance = Calcu.calculation_2point(str(self.destination_list[i]), str(self.destination_list[j]))
                    self.sheet_path.write(i, j, label=str(path))
                    self.sheet_path.write(j, i, label=str(path[::-1]))
                    # distance = len(eval(self.sheet_path.cell_value(i, j)))
                    self.sheet_distance.write(i, j, label = distance)
                    self.sheet_distance.write(j, i, label= distance)
        self.book.save(para.map_info_file)  # save the excel document

    def get_map_info(self, start, via_point, end):
        distance1 = self.get_2p_info(start, via_point)
        distance2 = self.get_2p_info(via_point, end)
        distance = distance1 + distance2
        return distance1, distance

    def get_2p_info(self, start, end):
        # assume the excel file and sheets has been opened yet
        index_start = self.destination_list.index(start)
        index_end = self.destination_list.index(end)
        distance = int(self.sheet_distance.cell_value(index_start, index_end))
        return distance


# if __name__ == '__main__':
#     path_file = open(para.path_file, "r")
#     path_list = path_file.readlines()
#     my_map_info = Map_info(path_list)
#     my_map_info.count_map_info()


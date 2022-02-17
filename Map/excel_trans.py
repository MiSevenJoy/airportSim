from Path_Calculation import Calculation
import xlrd
import xlwt
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
        self.destination_list = path_list[1]+path_list[2]+path_list[3]+path_list[4]
        # check whether the map-information excel file has generated

        if os.path.exists(para.map_info_file):
            self.book = xlrd.open_workbook(para.map_info_file)
            self.sheet_path = self.book.sheet_by_index(0)
            # self.sheet_distance = self.book.sheet_by_index(1)
        else:
            self.book = None
            self.sheet_path = None
            # self.sheet_distance = None
            self.count_map_info(path_list)


    def count_map_info(self, path_list):
        # format translation:translate the excel to path list
        # Trans = Excel_to_List(para.map_file, para.airport_name)
        # path_list = Trans.excel_to_pathlist()

        Calcu = Calculation(path_list[0])
        self.book = xlwt.Workbook()
        self.sheet_path = self.book.add_sheet(para.airport_name + ' path')
        # self.sheet_distance = self.book.add_sheet(para.airport_name + 'distance')
        total_number = len(self.destination_list)
        # count the all distance between two points by traversing
        for i in range(total_number):
            for j in range(i, total_number):
                if i == j:
                    self.sheet_path.write(i, j, label = None)
                    # self.sheet_distance.write(i, j, label = str(0))
                else:
                    path = Calcu.calculation_2point(str(self.destination_list[i]), str(self.destination_list[j]),path_list[0])[0]
                    self.sheet_path.write(i, j, label=str(path))
                    self.sheet_path.write(j, i, label=str(path[::-1]))
                    # self.sheet_distance.write(i, j, label = str(distance))
                    # self.sheet_distance.write(j, i, label=str(distance))
        self.book.save(para.map_info_file)  # save the excel document

    def get_map_info(self, start, via_point, end):
        # assume the excel file and sheets has been opened yet
        index_start = self.destination_list.index(start)
        index_via_point = self.destination_list.index(via_point)
        index_end = self.destination_list.index(end)
        # distance = int(float(self.sheet_distance.cell_value(index_start, index_via_point))) + int(float(self.sheet_distance.cell_value\
        # (index_via_point, index_end)))

        # delete the repetitive point
        first_list = eval(self.sheet_path.cell_value(index_start, index_via_point))
        # delete the repeated location
        first_list.pop()
        path = first_list + eval(self.sheet_path.cell_value(index_via_point, index_end))
        distance = len(path)-1

        return path, distance


if __name__ == '__main__':
    my_map = Excel_to_List(para.map_file, para.airport_name, para.rows, para.cols)
    my_map.excel_to_pathlist()


import Path_Calculation
import xlrd
import xlwt
import numpy as np
# the index of xls starts from 1 when using openpyxl
from Common import parameter as para
import os

'''
functions needed to be achieved in the file:
  1.read the map excel's colors as the path information
  2.background image generation
  3.preparation for the (least path length calculation)
'''

# use openpyxl instead of xlrd
'''
transfer the excel file to the path list information
'''
class Excel_to_List(object):

    def __init__(self, file_name, sheet_name):
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.book = None
        self.xf_list = None
        self.colour_map = None
        self.s = None

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
        rows = self.s.nrows  # 总行数
        cols = self.s.ncols  # total columns

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
        for i in range(0, rows):
            for j in range(0, cols):
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
        return list_path, list_near_p, list_far_p, list_bus_p, package_center

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

class List_to_NodeGraph(object):
    def __init__(self, map):
        self.map = map
        self.node_num = len(map)

    def node_name(self):               # labels为节点名称
        labels = []
        for i in range(0,self.node_num):
            labels.append(str(self.map[i]))
        return labels

    def map_nodegraph(self):
        graph = np.zeros(shape=(self.node_num,self.node_num))
        for i in range(0,self.node_num):
            for j in range(0,self.node_num):
                if i==j:
                    graph[i][j] = 0
                else:
                    pos_i = np.array(self.map[i])
                    pos_j = np.array(self.map[j])
                    x_pos_i = pos_i[0]
                    y_pos_i = pos_i[1]
                    x_pos_j = pos_j[0]
                    y_pos_j = pos_j[1]
                    if (abs(x_pos_i-x_pos_j)==0 and abs(y_pos_j-y_pos_i)==1) or \
                            (abs(x_pos_i-x_pos_j)==1 and abs(y_pos_j-y_pos_i)==0):
                        graph[i][j] = 1
                    else:
                        graph[i][j] = float('inf')
        return graph


'''
use nodegraph and labels to generate the graph of the map
'''
class NodeGraph_to_Graph:

    def __init__(self, nodegraph, labels):  # labels为标点名称
        self.Arcs = nodegraph
        self.VertexNum = nodegraph.shape[0]
        self.labels = labels


# directly get the path and distance of scheduling route
class Map_info:
    def __init__(self, path_list):
        # check whether the map-information excel file has generated
        self.path_list = path_list
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

        Calcu = Path_Calculation.Calculation(self.path_list[0])
        self.book = xlwt.Workbook()
        self.sheet_path = self.book.add_sheet(para.airport_name + ' path')
        self.sheet_distance = self.book.add_sheet(para.airport_name + 'distance')

        # get all destination that shuffle bus or luggage van may go to
        destination_list = self.path_list[1]+self.path_list[2]+self.path_list[3]+self.path_list[4]
        total_number = len(destination_list)
        # count the all distance between two points by traversing
        for i in range(total_number):
            for j in range(i, total_number):
                if i == j:
                    self.sheet_path.write(i, j, label = None)
                    self.sheet_distance.write(i, j, label = str(0))

                else:
                    path, distance = Calcu.calculation_2point(destination_list[i], destination_list[j], self.path_list[0])
                    self.sheet_path.write(i, j, label = str(path))
                    self.sheet_path.write(j, i, label=str(path.reverse()))
                    self.sheet_distance.write(i, j, label = str(distance))
                    self.sheet_distance.write(j, i, label=str(distance))
        self.book.save(para.map_info_file)  # save the excel document

    def get_map_info(self, start, via_point, end):
        # assume the excel file and sheets has been opened yet
        index_start = self.path_list.index(start)
        index_via_point = self.path_list.index(via_point)
        index_end = self.path_list.index(end)
        distance = int(self.sheet_distance.cell_value(index_start, index_via_point)) + int(self.sheet_distance.cell_value\
        (index_via_point, index_end))
        # delete the repetitive point
        path = eval(self.sheet_path.cell_value(index_start, index_via_point)).pop() + eval(self.sheet_path.cell_value\
        (index_via_point, index_end))

        return distance, path

from excel_trans import *
from Dijkstra import *

class Calculation():
    def __init__(self, map):
        self.graph = List_to_NodeGraph(map)
        self.nodegraph = self.graph.map_nodegraph()  # 节点二维数组
        self.labels = self.graph.node_name()  # 节点名称：节点坐标的字符形式
        self.G = NodeGraph_to_Graph(self.nodegraph, self.labels)
    def calculation_2point(self, start, endnode, map):
        dist, path = Dijkstra(self.G, self.G.labels.index(start), self.G.labels.index(endnode))
        Path = []
        Path1 = []
        for i in range(len(path)):
            Path.append(self.G.labels[path[len(path) - 1 - i]])  # Path为最短路径（列表格式，列表元素为字符串）
        for point in Path:
            Path1.append(map[self.labels.index(point)])          # Path1为最短路径（列表格式，列表元素为列表）
        return Path1, dist

    def calculation_3point(self, start, middle, end, map_name):
        path1, dist1 = self.calculation_2point(start, middle, map_name)
        path2, dist2 = self.calculation_2point(middle, end, map_name)
        path1.pop()                   # 删除path1中的最后一个元素
        path1.extend(path2)
        dist = dist1 + dist2
        return path1, dist-1
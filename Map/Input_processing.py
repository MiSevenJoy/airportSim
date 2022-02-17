import copy
import pandas as pd
import numpy as np
from Common import parameter as para
import os
from random import randrange


class Data_Process:
    def __init__(self):
        self.path = para.original_flight_data

    def time2min(self, _time):
        '''
        时间类型时分秒转换成分
        '''
        h = _time.hour  # 直接用datetime.time模块内置的方法，得到时、分、秒
        m = _time.minute
        # s = y.second
        return int(h) * 60 + int(m)  # int()函数转换成整数运算

    def extract_time_data(self):
        # extract the first two columns data
        time_data_depature = pd.read_excel(self.path, usecols=['计划出发时间', '实际出发时间'], sheet_name=para.sheet_name)
        time_data_arrive = pd.read_excel(self.path, usecols=['计划到达时间', '实际到达时间'], sheet_name=para.sheet_name)
        # delete the blank rows
        pure_t_data_depature = time_data_depature.dropna()
        pure_t_data_arrive = time_data_arrive.dropna()
        copy_data_depature = pure_t_data_depature.copy()
        copy_data_arrive = pure_t_data_arrive.copy()
        # translate the data format:from hh:mm:ss to minutes
        copy_data_depature.loc[:, '计划出发时间'] = copy_data_depature.loc[:, '计划出发时间'].apply(self.time2min)
        copy_data_depature.loc[:, '实际出发时间'] = copy_data_depature.loc[:, '实际出发时间'].apply(self.time2min)
        copy_data_arrive.loc[:, '计划到达时间'] = copy_data_arrive.loc[:, '计划到达时间'].apply(self.time2min)
        copy_data_arrive.loc[:, '实际到达时间'] = copy_data_arrive.loc[:, '实际到达时间'].apply(self.time2min)
        # rename the columns
        copy_data_depature.columns = ['schedule_time', 'actual_time']
        copy_data_arrive.columns = ['schedule_time', 'actual_time']
        # add the flight type column to the dataframe
        copy_data_depature.insert(2, 'flight_type', [1 for _ in range(copy_data_depature.shape[0])])
        copy_data_arrive.insert(2, 'flight_type', [0 for _ in range(copy_data_arrive.shape[0])])
        t_data = pd.concat([copy_data_depature, copy_data_arrive])
        t_data = t_data.sort_values(by='schedule_time')

        return t_data

    def extract_refer_delay_t(self,data):
        new_t_data = np.array(data.copy())
        delete_list = []
        for i in range(len(new_t_data)):
            if abs(new_t_data[i,0] - new_t_data[i,1])>para.delay_t:
                delete_list.append(i)
        # new_t_data = pd.DataFrame(np.delete(new_t_data, delete_list, 0))
        new_t_data = np.delete(new_t_data, delete_list, 0)
        return new_t_data

    def write_to_excel(self, path, data_write, page, start_row, start_col):
        if not os.path.exists(path):
            data_write.to_excel(
                path,
                page,
                index=False,
                startrow=start_row,
                startcol=start_col
            )
        else:
            with pd.ExcelWriter(
                    path,
                    engine='openpyxl',
                    mode='a'
            ) as writer:
                data_write.to_excel(
                    writer,
                    page,
                    index=False,
                    startrow=start_row,
                    startcol=start_col
            )

    def grouping(self, data_array):
        # add the information of using parking lot start-time
        start_t_data = np.empty([len(data_array), 1], dtype=int)
        for i in range(len(data_array)):
            if data_array[i, 2] == 1:
                start_t_data[i, 0] = data_array[i, 0]-50
            else:
                start_t_data[i, 0] = data_array[i, 0] -15
        new_t_data = np.insert(data_array, [3], start_t_data, axis=1)
        new_t_data = new_t_data[np.argsort(new_t_data[:,3])]

        # grouping data into several groups to make sure the data is less than the airport's capacity
        page_index = 0
        episode_list =[]
        while len(new_t_data)>1:
            move_list = []
            episode = np.empty(shape=(0, 4),dtype=int)
            start_item = new_t_data[0]
            start_index = 0
            i = 0
            while i < len(new_t_data)-1:
                for i in range(start_index, len(new_t_data)):
                    if new_t_data[i, 3]-start_item[3] > 60:
                        break
                len_episode = i - start_index
                if len_episode > para.n_flight:
                    # random select n_flight rows from len_episode rows
                    e_move_list = np.random.choice([j for j in range(start_index, i)], para.n_flight, replace=False)
                    e_move_list = np.sort(e_move_list).tolist()
                    episode = np.row_stack([episode, new_t_data[e_move_list]])

                else:
                    # all rows are selected
                    e_move_list = [j for j in range(start_index, i)]
                    episode = np.row_stack([episode, new_t_data[start_index:i, :]])
                start_index = i
                start_item = new_t_data[i]
                move_list.extend(e_move_list)
            episode_list.append(episode)
                # episode = pd.DataFrame(episode)
                # episode = episode[[0, 1, 2]]
                # self.write_to_excel(para.flight_data, episode, 'page_'+str(page_index), ['schedule_t, actual,t flight_type'], 0, 0)
                # self.write_to_excel(para.flight_data, episode, 'page_' + str(page_index),
                #                     ['schedule_t', 'actual_t',' flight_type', 'start_park_t'], 0, 0)
            new_t_data = np.delete(new_t_data, move_list, 0)
            page_index += 1
        return episode_list

    def dispatch_parking_lot(self, data_array):
        """
        :param data_array: time data array got from function grouping
        :return: data_array+park_plan(aircraft parking lot's and passenger parking position)
        """
        # sort by the time of starting parking
        park_plan = np.zeros([len(data_array), 2], dtype=int)
        #
        # new_t_data = data_array[np.argsort(data_array[:, 3])]

        # use a dictionary to store the parking lots
        aircraft_parks = {i: [] for i in range(para.n_parking_lot)}
        passenger_in_parks = {i: [] for i in range(para.n_passenger_lot)}
        passenger_out_parks = {i: [] for i in range(para.n_passenger_lot)}
        for j in range(len(data_array)):
            flag = 1
            while flag == 1:
                choice = randrange(para.n_parking_lot)
                if len(aircraft_parks[choice]) == 0 or data_array[j, 3] > aircraft_parks[choice][1]:
                    aircraft_parks[choice] = [data_array[j][3], data_array[j][3] + 60]
                    park_plan[j, 0] = choice
                    flag = 0
            flag = 1
            while flag == 1:
                if data_array[j, 2] == 0:
                    choice = randrange(para.n_passenger_lot)
                    if len(passenger_in_parks[choice]) == 0 or data_array[j, 3] > passenger_in_parks[choice][1]:
                        passenger_in_parks[choice] = [data_array[j][3], data_array[j][3] + 60]
                        park_plan[j, 1] = choice
                        flag = 0
                else:
                    choice = randrange(para.n_passenger_lot)
                    if len(passenger_out_parks[choice]) == 0 or data_array[j, 3] > passenger_out_parks[choice][1]:
                        passenger_out_parks[choice] = [data_array[j][3], data_array[j][3] + 60]
                        park_plan[j, 1] = choice
                        flag = 0

        t_data = np.insert(data_array[:, 0:3], [3], park_plan, axis=1)
        return t_data

    def generate_vehicles(self, data_array):
        """
        :param data_array: time data array from function dispatch_parking_lot
        :return: completed flight data(DataFrame)
        """
        number = len(data_array)
        luggage_van_list = np.random.randint(1, 2, (number, 1), dtype=int)
        shuttle_list = np.random.randint(1, 3, (number, 1), dtype=int)
        data_array = np.insert(data_array, [5], shuttle_list, axis=1)
        data_array = np.insert(data_array, [6], luggage_van_list, axis=1)
        flight_data = data_array[np.argsort(data_array[:, 0])]
        flight_data = pd.DataFrame(flight_data)
        flight_data.columns = ['scheduled departure/arrive time', 'actual departure/arrive time', 'type','aircraft park'
                  'ing lot', 'passenger departure/arrival port', 'shuttle number needed', 'luggage van  number needed']
        return flight_data

    def generate_tasks(self, flight_data, aircraft_p_list, passenger_p_list, package_center):
        task_data = pd.DataFrame(columns=['flight number', 'scheduled departure/arrive time', 'actual departure/arrive '
                                          'time', 'origin', 'via point', 'end', 'type(shuttle/luggage van)'])
        for i in range(len(flight_data)):
            task_data_list = [i]
            task_data_list.extend(flight_data.iloc[i, 0:2].values.tolist())
            task_data_list.append(None)
            task_data_list_copy = copy.deepcopy(task_data_list)
            shuttle_path = [passenger_p_list[flight_data.iloc[i, 4]], aircraft_p_list[flight_data.iloc[i, 3]]]
            luggage_van_path = [package_center[0], aircraft_p_list[flight_data.iloc[i, 3]]]
            if flight_data.iloc[i, 2] == 1:
                task_data_list.extend(shuttle_path)
                task_data_list_copy.extend(luggage_van_path)
            else:
                task_data_list.extend(shuttle_path[::-1])
                task_data_list_copy.extend(luggage_van_path[::-1])
            task_data_list.append('shuttle')
            task_data_list_copy.append('luggage van')
            for j in range(flight_data.iloc[i, 5]):
                task_data.loc[len(task_data)] = task_data_list
            for k in range(flight_data.iloc[i, 6]):
                task_data.loc[len(task_data)] = task_data_list_copy
        return task_data

    def data_preparation(self, aircraft_p_list, passenger_p_list, package_center):
        # extract time data from flight table
        data1 = self.extract_time_data()
        # delete the flights that delays/ ahead of time too much
        data2 = self.extract_refer_delay_t(data1)
        # grouping referring to the time of starting using the aircraft parking lot
        data3_list = self.grouping(data2)
        i = 1
        for data in data3_list:
            data4 = self.dispatch_parking_lot(data)
            data_flight = self.generate_vehicles(data4)
            data_task = self.generate_tasks(data_flight, aircraft_p_list, passenger_p_list, package_center)
            self.write_to_excel(para.flight_data, data_flight, para.sheet_name+'_'+str(i), 0, 0)
            self.write_to_excel(para.task_data, data_task, para.sheet_name+'_'+str(i), 0, 0)
            i += 1



if __name__ =='__main__':
    my_data_process = Data_Process()
    my_data_process.data_preparation(path_list[1]+path_list[2], path_list[1], path_list[4])
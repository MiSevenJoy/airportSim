import pygame

class Scen:
    def __init__(self,width, height, bg_name):
        self.screen = pygame.display.set_mode((width, height))
        self.bg = pygame.image.load(bg_name)
        self.screen.blit(self.bg, (0, 0))# (x, y) is the left up location

    def env_render(self):
        '''
        :param agent_group: the shuffle and package car group
        :param mark_group: the land mark group
        :return:
        '''
        self.screen.blit(self.bg, (0, 0))  # update the background image
        self.create_landmark()
        # update the display of logos
        # self.set_landmark()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("end simulation...")
                pygame.quit()
                exit(0)
        # update the display of cars and landmarks
        self.mark_group.draw(self.screen)
        self.bus_group.update(self.time)
        self.pc_group.update(self.time)
        self.bus_group.draw(self.screen)
        self.pc_group.draw(self.screen)

        # update the screen
        pygame.display.update()
        info_fmt = info.render("time:"+str(self.time), True, (0, 0, 0))
        self.screen.blit(info_fmt, (0, 0))
        # 更新屏幕
        pygame.display.flip()
        pygame.time.delay(100)
        # environment render once, env time +1

    # put the land_mark on the screen to display
    def create_landmark(self):
        j = 0
        for j in range(len(self.list_near_p)):
            locals()['mark' + str(j)] = agent.Agent(para.passenger_near_img, self.list_near_p[j], 2)
            self.mark_group.add(locals()['mark' + str(j)])
        number = j
        for j in range(number + 1, number + len(self.list_far_p) + 1):
            locals()['mark' + str(j)] = agent.Agent(para.park_point_img, self.list_far_p[j - number - 1], 2)
            self.mark_group.add(locals()['mark' + str(j)])
        locals()['mark' + str(j + 1)] = agent.Agent(para.package_center_img, self.package_center, 2)
        self.mark_group.add(locals()['mark' + str(j + 1)])

    # create bus and pc for the environment
    def create_bus_pc(self):
        for i in range(self.bus_n):
            if i < int(len(self.bus_n) / 2):
                locals()['bus' + str(i)] = agent.Agent(para.bus_img, self.list_bus_p[0], 0)
            else:
                locals()['bus' + str(i)] = agent.Agent(para.bus_img, self.list_bus_p[1], 0)
            self.bus_group.add(locals()['bus' + str(i)])
            self.bus_avai_group.add(locals()['bus' + str(i)])

        for j in range(self.pc_n):
            if j < int(len(self.bus_n) / 2):
                locals()['pc' + str(j)] = agent.Agent(para.pc_img, self.list_bus_p[2], 1)
            else:
                locals()['pc' + str(j)] = agent.Agent(para.pc_img, self.list_bus_p[3], 1)
            self.pc_group.add(locals()['pc' + str(j)])
            self.pc_avai_group.add(locals()['pc' + str(j)])
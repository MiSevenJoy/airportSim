import pygame

class Scen:
    def __init__(self,width, height, bg_name):
        self.screen = pygame.display.set_mode((width, height))
        self.bg = pygame.image.load(bg_name)
        self.screen.blit(self.bg, (0, 0))# (x, y) is the left up location
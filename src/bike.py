import pygame
from obstacle import Obstacle
class Bike(Obstacle):
    def __init__(self, x, y, width, height, color=(0, 0, 255), transparency = 100, passthrough=True):
        super().__init__(x, y, width, height, color, transparency, passthrough)
        self.is_house_flag = False
        self.is_bike_flag = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

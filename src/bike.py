import pygame
from src.obstacle import Obstacle
class Bike(Obstacle):
    def __init__(self, x, y, width, height, color=(0, 0, 255, 255), transparency = 100, passthrough=True):
        super().__init__(x, y, width, height, obstacle_type="bike", color=color, transparency=transparency, passthrough=passthrough)
        self.is_house_flag = False
        self.is_bike_flag = True

        self.image = pygame.image.load("assets/images/bike.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
import pygame
from obstacle import Obstacle
class Bike(Obstacle):
    def __init__(self, x, y, width, height, color=(0, 0, 255, 255), transparency = 100, passthrough=True):
        super().__init__(x, y, width, height, color, transparency, passthrough)
        self.is_house_flag = False
        self.is_bike_flag = True

        # Load PNG
        self.image = pygame.image.load("../assets/medium_rack.png").convert_alpha()

        # Scale PNG to fit the cube
        self.image = pygame.transform.scale(self.image, (width, height))

        # Make sure rect is correct
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
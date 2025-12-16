import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(0, 0, 255), transparency = 100, passthrough=False):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.image.set_alpha(transparency)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.passthrough = passthrough
        self.is_house_flag = True
        self.is_bike_flag = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def collides_with(self, player_rect):
        return self.rect.colliderect(player_rect)

    def is_passthrough(self):
        return self.passthrough

    def is_bike(self):
        return self.is_bike_flag

    def is_house(self):
        return self.is_house_flag
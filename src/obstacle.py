import pygame

class Obstacle:
    def __init__(self, x, y, width, height, passthrough=False):
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.passthrough = passthrough

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def collides_with(self, player_rect):
        return self.rect.colliderect(player_rect)

import pygame

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.camera_width = width
        self.camera_height = height

    def apply(self, entity):
        # Move the entity's rect by the camera's position
        return entity.rect.move(self.camera.topleft)

    def update(self, target, screen_width, screen_height):
        x = -target.rect.centerx + screen_width // 2
        y = -target.rect.centery + screen_height // 2

        # Keep the camera within the bounds of the world
        # x = min(0, x)
        # y = min(0, y)
        # x = max(-(self.camera_width - screen_width), x)
        # y = max(-(self.camera_height - screen_height), y)

        self.camera = pygame.Rect(x, y, self.camera_width, self.camera_height)

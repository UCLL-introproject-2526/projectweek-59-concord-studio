import pygame

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.offset = pygame.Vector2(0, 0)
        self.camera_width = width
        self.camera_height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)


    def follow(self, target):
        self.offset.x = target.rect.centerx - self.camera_width // 2
        self.offset.y = target.rect.centery - self.camera_height // 2

        self.offset.x = max(0, self.offset.x)
        self.offset.y = max(0, self.offset.y)

        # magic number for bg size, hardcoded for now
        self.offset.x = min(7390, self.offset.x)
        self.offset.y = min(7590, self.offset.y)
        #print(self.offset.x, self.offset.y)

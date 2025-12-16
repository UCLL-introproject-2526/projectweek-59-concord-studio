import pygame

class Police(pygame.sprite.Sprite):
    def __init__(self, x, y, speed = 3):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 0))
        self.image.set_alpha(190)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self, target_rect):
        epsilon = 5
        if abs(self.rect.x - target_rect.x) > epsilon:
            if self.rect.x < target_rect.x:
                self.rect.x += self.speed
            elif self.rect.x > target_rect.x:
                self.rect.x -= self.speed
        if abs(self.rect.y - target_rect.y) > epsilon:
            if self.rect.y < target_rect.y:
                self.rect.y += self.speed
            elif self.rect.y > target_rect.y:
                self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_position(self):
        return self.rect.topleft

    def set_position(self, position):
        self.rect.topleft = position
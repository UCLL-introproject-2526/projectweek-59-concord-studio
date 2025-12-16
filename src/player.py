import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def update(self, keys):
        #keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_position(self):
        return self.rect.topleft

    def set_position(self, position):
        self.rect.topleft = position

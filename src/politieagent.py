# politieagent.py
import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=2):
        super().__init__()

        # load image
        image = pygame.image.load("../assets/police_running.png").convert_alpha()
        # scale it
        image = pygame.transform.scale(image, (64, 64))
        # assign to sprite
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = speed

    def update(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed

        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed

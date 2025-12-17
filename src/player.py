import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5):
        super().__init__()

        self.image_normal = pygame.image.load("../assets/thief.png").convert_alpha()
        self.image_normal = pygame.transform.scale(self.image_normal, (140, 76))
    
        self.image_bike = pygame.image.load("../assets/bike_hold.png").convert_alpha()
        self.image_bike = pygame.transform.scale(self.image_bike, (170, 106))

        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed


        # thief_size = pygame.transform.scale(self.image, (self.image.get_size()[0] * 1, self.image.get_size()[1] * 1)).convert()
        # self.image = thief_size.convert_alpha()
        # self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

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
        if keys[pygame.K_LSHIFT]:
            self.speed = 1
        else:
            self.speed = 5

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_position(self):
        return self.rect.topleft

    def set_position(self, position):
        self.rect.topleft = position

    def get_rect(self):
        return self.rect
    

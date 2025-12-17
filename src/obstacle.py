import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, obstacle_type="house", color=(0, 0, 255), transparency=100, passthrough=False):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.image.set_alpha(transparency)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.obstacle_type = obstacle_type
        self.passthrough = passthrough
        
        self.interaction_radius = 40

        self.is_house_flag = (obstacle_type == "house")
        self.is_bike_flag = (obstacle_type == "bike")

    def can_interact(self, player_rect):
        if self.obstacle_type != "water":
            return False
            
        interaction_zone = self.rect.inflate(self.interaction_radius, self.interaction_radius) 
        return interaction_zone.colliderect(player_rect)

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
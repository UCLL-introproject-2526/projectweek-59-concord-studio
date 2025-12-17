import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5):
        super().__init__()

        # Load normal sprite
        self.image_normal = pygame.image.load("../assets/thief.png").convert_alpha()
        self.image_normal = pygame.transform.scale(self.image_normal, (76, 76))

        # Load bike sprite
        self.image_bike = pygame.image.load("../assets/bike_hold.png").convert_alpha()
        self.image_bike = pygame.transform.scale(self.image_bike, (90, 90))

        # Load running animation sprites
        self.run_sprites = [
            pygame.transform.scale(pygame.image.load("../assets/thief_run_1.png").convert_alpha(), (76, 76)),
            pygame.transform.scale(pygame.image.load("../assets/thief_run_2.png").convert_alpha(), (76, 76))
        ]

        self.current_frame = 0
        self.last_update = 0
        self.animation_delay_holding_bike = 500

        self.run_with_bike = [
            pygame.transform.scale(pygame.image.load("../assets/bike_hold_run_1.png").convert_alpha(), (90, 90)),
            pygame.transform.scale(pygame.image.load("../assets/bike_hold_run_2.png").convert_alpha(), (90, 90))
        ]

        #VERY IMPORTANT!!! DON'T DELETE CODE BELOW!!!

        # self.current_frame = 0
        # self.last_update = 0
        # self.animation_duration_throwing_bike = 200

        # self.bike_throw = pygame.transform.scale(pygame.image.load("../assets/bike_throw.png").convert_alpha(), (90, 90))

        # Current image and rect
        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

        # Animation variables
        self.current_frame = 0
        self.last_update = 0
        self.animation_delay_normal = 300  # milliseconds between frames



        # thief_size = pygame.transform.scale(self.image, (self.image.get_size()[0] * 1, self.image.get_size()[1] * 1)).convert()
        # self.image = thief_size.convert_alpha()
        # self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, keys, held_bike):
        moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            moving = True

        if keys[pygame.K_LSHIFT]:
            self.speed = 1
        else:
            self.speed = 5

        now = pygame.time.get_ticks()
        if held_bike and moving:
    # If holding a bike, show bike sprite
            if now - self.last_update > self.animation_delay_holding_bike:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_with_bike)
                self.image = self.run_with_bike[self.current_frame]
        elif moving:
            # Running animation
            if now - self.last_update > self.animation_delay_normal:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_sprites)
                self.image = self.run_sprites[self.current_frame]
        # elif throwing:
        #     # Running animation
        #     if now - self.last_update > self.animation_duration_throwing_bike:
        #         self.last_update = now
        #         self.current_frame = (self.current_frame + 1) % len(self.bike_throw)
        #         self.image = self.bike_throw[self.current_frame]


    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_position(self):
        return self.rect.topleft

    def set_position(self, position):
        self.rect.topleft = position

    def get_rect(self):
        return self.rect
    

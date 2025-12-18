import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=5):
        super().__init__()

        self.facing_right = True
        self.speed = speed

        # Load normal sprite
        self.image_normal = pygame.image.load("assets/images/thief.png").convert_alpha()
        self.image_normal = pygame.transform.scale(self.image_normal, (76, 76))

        # Load bike sprite
        self.image_bike = pygame.image.load("assets/images/bike_hold.png").convert_alpha()
        self.image_bike = pygame.transform.scale(self.image_bike, (100, 100))

        # Load running animation sprites
        self.run_sprites = [
            pygame.transform.scale(pygame.image.load("assets/images/thief_run_1.png").convert_alpha(), (76, 76)),
            pygame.transform.scale(pygame.image.load("assets/images/thief_run_2.png").convert_alpha(), (76, 76))
        ]

        self.current_frame = 0
        self.last_update = 0
        self.animation_delay_holding_bike = 500

        self.run_with_bike = [
            pygame.transform.scale(pygame.image.load("assets/images/bike_hold_run_1.png").convert_alpha(), (100, 100)),
            pygame.transform.scale(pygame.image.load("assets/images/bike_hold_run_2.png").convert_alpha(), (100, 100))
        ]

        self.bike_throw = [
            pygame.transform.scale(pygame.image.load(f"assets/images/bike_throw.png").convert_alpha(),(135, 90))
        ]

        self.throwing_bike = False
        self.current_frame = 0
        self.last_update = 0
        self.animation_duration_throwing_bike = 300  # ms

        # Current image and rect
        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

        # Animation variables
        self.current_frame = 0
        self.last_update = 0
        self.animation_delay_normal = 300  # milliseconds between frames
    
    def apply_direction(self, image):
        if not self.facing_right:
            return pygame.transform.flip(image, True, False)
        return image
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, keys, held_bike):
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.facing_right = False
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.facing_right = True
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            moving = True

        self.speed = 1 if keys[pygame.K_LSHIFT] else 5

        now = pygame.time.get_ticks()

        if self.throwing_bike:
            if now - self.last_update > self.animation_duration_throwing_bike:
                self.last_update = now
                self.current_frame += 1
                if self.current_frame >= len(self.bike_throw):
                    self.throwing_bike = False
                    self.image = self.apply_direction(self.image_normal if not held_bike else self.image_bike)
                else:
                    self.image = self.apply_direction(
                        self.bike_throw[self.current_frame]
                    )
        elif held_bike and moving:
            if now - self.last_update > self.animation_delay_holding_bike:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_with_bike)
                self.image = self.apply_direction(
                    self.run_with_bike[self.current_frame]
                )
        elif moving:
            if now - self.last_update > self.animation_delay_normal:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.run_sprites)
                self.image = self.apply_direction(
                    self.run_sprites[self.current_frame]
                )
        else:
            self.image = self.apply_direction(
                self.image_bike if held_bike else self.image_normal
            )

    def start_throw_animation(self):
        self.throwing_bike = True
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.image = self.apply_direction(self.bike_throw[0])


    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_position(self):
        return self.rect.topleft

    def set_position(self, position):
        self.rect.topleft = position

    def get_rect(self):
        return self.rect
    

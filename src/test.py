import pygame

class Camera:
    def __init__(self, width, height):
        self.offset = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def follow(self, target):
        # Center the camera on the target
        self.offset.x = target.rect.centerx - self.width // 2
        self.offset.y = target.rect.centery - self.height // 2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed


def draw(screen, camera, sprites):
    for sprite in sprites:
        screen.blit(
            sprite.image,
            sprite.rect.topleft - camera.offset
        )


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, passthrough=False):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.passthrough = passthrough


    def collides_with(self, player_rect):
        return self.rect.colliderect(player_rect)


screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player = Player(400, 300)
camera = Camera(800, 600)
obs = Obstacle(200, 200, 100, 100)
bg = pygame.image.load('../assets/background.png')
bgBig = pygame.transform.scale(bg, (2272 * 2, 1888 * 2))

sprites = pygame.sprite.Group(player, obs)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.update(keys)

    camera.follow(player)

    screen.fill((30, 30, 30))
    screen.blit(bgBig, (0, 0))

    draw(screen, camera, sprites)
    pygame.display.flip()

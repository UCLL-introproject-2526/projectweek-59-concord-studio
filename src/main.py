import pygame
from player import Player
from obstacle import Obstacle
from camera import Camera


def draw(screen, camera, sprites, bgBig = None, bg_rect = None):
    if bgBig and bg_rect:
        screen.blit(bgBig, bg_rect.topleft - camera.offset)

    for sprite in sprites:
        screen.blit(
            sprite.image,
            sprite.rect.topleft - camera.offset
        )

def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    bg = pygame.image.load('../assets/background.png')
    bgBig = pygame.transform.scale(bg, (bg.get_size()[0] * 2, bg.get_size()[1] * 2)).convert()
    world_width, world_height = bgBig.get_size()
    print(world_width, world_height)

    pygame.display.set_caption("No Lock, No Mercy")
    clock = pygame.time.Clock()
    icon = pygame.image.load('../assets/bike_holding.png')
    pygame.display.set_icon(icon)
    running = True

    camera = Camera(screen_width, screen_height)
    player = Player(300, 300)
    obstacles = [Obstacle(100, 100, 200, 50), Obstacle(350, 100, 200, 50)]

    sprites = pygame.sprite.Group(player, obstacles)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos() + camera.offset)

        old_position = player.get_position()
        #player.update()
        keys = pygame.key.get_pressed()
        player.update(keys)
        camera.follow(player)
        #camera.update(player, screen_width, screen_height)
        screen.fill((255, 255, 255))
        #screen.blit(bgBig, (0, 0))



        for obstacle in obstacles:
            #obstacle.draw(screen)
            if obstacle.collides_with(player.rect):
                print("Collision detected!")
                player.set_position(old_position)
        # player out of bounds
        if player.rect.left < 0 or player.rect.right > world_width or player.rect.top < 0 or player.rect.bottom > world_height:
            player.set_position(old_position)

        draw(screen, camera, sprites, bgBig, bgBig.get_rect())
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()


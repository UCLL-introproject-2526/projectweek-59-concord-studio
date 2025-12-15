import pygame
from player import Player
from obstacle import Obstacle
from camera import Camera

def main():
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    bg = pygame.image.load('../assets/background.png')
    bgBig = pygame.transform.scale(bg, (2272 * 2, 1888 * 2))

    pygame.display.set_caption("No Lock, No Mercy")
    clock = pygame.time.Clock()
    running = True

    camera = Camera(1600, 1200)
    player = Player(0, 0)
    obstacles = [Obstacle(100, 100, 200, 50), Obstacle(350, 100, 200, 50)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        old_position = player.get_position()
        player.handle_keys()
        camera.update(player, screen_width, screen_height)

        screen.fill((255, 255, 255))
        screen.blit(bgBig, (0, 0))

        player.draw(screen)

        for obstacle in obstacles:
            obstacle.draw(screen)
            if obstacle.collides_with(player.rect):
                print("Collision detected!")
                player.set_position(old_position)



        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()


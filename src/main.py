import pygame
from player import Player
from obstacle import Obstacle
from camera import Camera
from hitbox import Hitbox
from bike import Bike
from menu import show_menu

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

show_menu(screen, screen_width, screen_height)

def draw(screen, camera, sprites, bgBig = None, bg_rect = None):
    if bgBig and bg_rect:
        screen.blit(bgBig, bg_rect.topleft - camera.offset)

    for sprite in sprites:
        screen.blit(
            sprite.image,
            sprite.rect.topleft - camera.offset
        )

def main():
    # pygame.init()

    # screen_width = 800
    # screen_height = 600
    # screen = pygame.display.set_mode((screen_width, screen_height))

    bg = pygame.image.load('../assets/background.png')
    bgBig = pygame.transform.scale(bg, (bg.get_size()[0] * 2, bg.get_size()[1] * 2)).convert()
    world_width, world_height = bgBig.get_size()
    print(world_width, world_height)

    pygame.display.set_caption("No Lock, No Mercy")
    clock = pygame.time.Clock()
    icon = pygame.image.load('../assets/bike_holding.png')
    pygame.display.set_icon(icon)
    running = True
    colliding_Bike = None
    picked_up_bike = None

    camera = Camera(screen_width, screen_height)
    player = Player(300, 300)
    obstacles = [Obstacle(100, 100, 200, 50), Obstacle(350, 100, 200, 50),
                 Bike(100, 300, 100, 50, color=(0, 255, 0), transparency=150)]

    sprites = pygame.sprite.Group(player, obstacles)

    # hitbox_objects = Hitbox.load_map_objects('../assets/hitbox_map.png')
    # for obj in hitbox_objects:
    #     if obj['type'] == 'house' or obj['type'] == 'water':
    #         obstacle = Obstacle(
    #             obj['rect'].x,
    #             obj['rect'].y,
    #             obj['rect'].width,
    #             obj['rect'].height
    #         )
    #         obstacles.append(obstacle)
    #         sprites.add(obstacle)

    # print(f"Loaded {len(hitbox_objects)} hitbox objects from map.")
    # print(hitbox_objects)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_e:
                    if colliding_Bike and not picked_up_bike:
                        picked_up_bike = colliding_Bike
                        sprites.remove(colliding_Bike)
                        obstacles.remove(colliding_Bike)
                        print("Picked up the bike!")
                    elif picked_up_bike:
                        picked_up_bike.rect.topleft = player.rect.topleft
                        sprites.add(picked_up_bike)
                        obstacles.append(picked_up_bike)
                        print("Dropped the bike!")
                        picked_up_bike = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if colliding_Bike:
                    print("Interacted with bike!")
                    print(colliding_Bike)

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
                if not obstacle.is_passthrough():
                    player.set_position(old_position)
                if obstacle.is_bike():
                    colliding_Bike = obstacle
            else:
                colliding_Bike = None

        # player out of bounds
        if player.rect.left < 0 or player.rect.right > world_width or player.rect.top < 0 or player.rect.bottom > world_height:
            player.set_position(old_position)

        draw(screen, camera, sprites, bgBig, bgBig.get_rect())
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()


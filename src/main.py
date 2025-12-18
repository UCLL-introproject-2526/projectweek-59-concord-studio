import pygame
from player import Player
from obstacle import Obstacle
from camera import Camera
from hitbox import Hitbox
from bike import Bike
#from menu import show_menu
from police import Police
#from end_screen import show_end_screen
from soundmanager import SoundManager
import random
import menu
import end_screen
import asyncio

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
    
    #top left Icon GMH
    icon = pygame.image.load('../assets/images/cop_run_1.png')
    pygame.display.set_icon(icon)


    menu.show_menu(screen, screen_width, screen_height)

    bg = pygame.image.load('../assets/images/background.png')
    bgBig = pygame.transform.scale(bg, (bg.get_size()[0] * 2, bg.get_size()[1] * 2)).convert()
    world_width, world_height = bgBig.get_size()
    print(world_width, world_height)


    pygame.display.set_caption("No Lock, No Mercy")
    clock = pygame.time.Clock()
    sound = SoundManager()
    sound.play_sound("background", volume=0.5, loops=-1)




    running = True
    colliding_Bike = None
    picked_up_bike = None

    camera = Camera(screen_width, screen_height)
    player = Player(100, 900)
    possible_bike_positions = []
    possible_cop_positions = []
    obstacles = [] 
    police = []
    obstacles = [Bike(200, 900, 90, 60, color=(0, 255, 0), transparency=150, passthrough=True)]

    #score bored GMH
    score = 0
    pygame.font.init()
    score_font = pygame.font.SysFont("consolas", 36)  

    sprites = pygame.sprite.Group(player, *obstacles, *police, )

    hitbox_objects = Hitbox.load_map_objects('../assets/images/hitbox_map.png')
    print(len(hitbox_objects))
    for obj in hitbox_objects:
        if obj['type'] == 'house' or obj['type'] == 'water':
            obstacle = Obstacle(
                obj['rect'].x,
                obj['rect'].y,
                obj['rect'].width,
                obj['rect'].height,
                obstacle_type=obj['type'],
                transparency=150,
                passthrough=False
            )
            obstacles.append(obstacle)
            sprites.add(obstacle)
        elif obj['type'] == 'bike-spawn':
            possible_bike_positions.append((obj['rect'].x, obj['rect'].y))
        elif obj['type'] == 'cop':
            possible_cop_positions.append((obj['rect'].x, obj['rect'].y))
    print("cop len: ", len(possible_cop_positions))

    amount_of_bikes = 30
    bike_positions = random.sample(possible_bike_positions, min(amount_of_bikes, len(possible_bike_positions)))
    for pos in bike_positions:
        bike = Bike(pos[0], pos[1], 100, 50, color=(0, 255, 0), transparency=150)
        obstacles.append(bike)
        sprites.add(bike)
        print(pos)

    amount_of_cops = 5 
    if possible_cop_positions:
        cop_positions = random.sample(possible_cop_positions, min(amount_of_cops, len(possible_cop_positions)))
        for pos in cop_positions:
            new_cop = Police(pos[0], pos[1], hitbox_objects, spawn_pos=pos)
            police.append(new_cop)
            print("police:", pos)
    sprites = pygame.sprite.Group(player, obstacles, police)

    # print(f"Loaded {len(hitbox_objects)} hitbox objects from map.")
    # print(hitbox_objects)
    while running:
        #sound.play_sound("start_up_sfx")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_e:
                    near_water = any(obs.can_interact(player.rect) for obs in obstacles)

                    if picked_up_bike and near_water:
                        print("You threw the bike in the water.")
                        player.image = player.image_normal
                        picked_up_bike = None
                        score += 100
                    elif colliding_Bike and not picked_up_bike:
                        picked_up_bike = colliding_Bike
                        sprites.remove(colliding_Bike)
                        obstacles.remove(colliding_Bike)
                        player.image = player.image_bike
                        colliding_Bike = None
                    elif picked_up_bike:
                        picked_up_bike.rect.topleft = player.rect.topleft
                        sprites.add(picked_up_bike)
                        obstacles.append(picked_up_bike)
                        player.image = player.image_normal
                        picked_up_bike = None

        old_pos_player = player.get_position()
        keys = pygame.key.get_pressed()
        player.update(keys, picked_up_bike)
        camera.follow(player)
        screen.fill((255, 255, 255))

        if picked_up_bike:
            for p in police:
                p.set_speed(3)
                p.update(player.get_rect())
        # else: # add timer so that cops dont instantly walk back to spawn
        #     for p in police:
        #         #p.set_speed(3)
        #         p.update(player.get_rect(), go_to_spawn=True)

        current_colliding_bike = None

        for obstacle in obstacles:
            if obstacle.collides_with(player.rect):

                if not obstacle.is_passthrough():
                    player.set_position(old_pos_player)

                if obstacle.is_bike():
                    current_colliding_bike = obstacle

        colliding_Bike = current_colliding_bike

        if picked_up_bike:
            for p in police:
                p.update(player.get_rect())
                if p.rect.colliderect(player.rect):
                    sound.play_sound("game_over") 
                    result = end_screen.show_end_screen(screen, screen_width, screen_height)
                    if result == "restart":
                        main()
                    return

        

        # player out of bounds
        if player.rect.left < 0 or player.rect.right > world_width or player.rect.top < 0 or player.rect.bottom > world_height:
            player.set_position(old_pos_player)

        draw(screen, camera, sprites, bgBig, bgBig.get_rect())
        #draw score gmh
        score_text = score_font.render(f"SCORE:{score}",True,(255,255,255))
        screen.blit(score_text,(10,10))

        pygame.display.flip()
        clock.tick(60)
        #await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    main()
    #asyncio.run(main())
    #asyncio.run(main())
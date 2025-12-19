import pygame
from src.player import Player
from src.obstacle import Obstacle
from src.camera import Camera
from src.hitbox import Hitbox
from src.bike import Bike
#from menu import show_menu
from src.police import Police
#from end_screen import show_end_screen
from src.soundmanager import SoundManager
import random
import src.menu
import src.end_screen
import asyncio
import math
import src.mini_map



async def main():
    icon = pygame.image.load('assets/images/cop_run_1.png')
    bg = pygame.image.load('assets/images/background.png')
    scoreBored_Path = 'assets/images/instructions_score_opacity.png'

    def draw(screen, camera, sprites, bgBig=None, bg_rect=None):
        if bgBig and bg_rect:
            screen.blit(bgBig, bg_rect.topleft - camera.offset)

        for sprite in sprites:
            screen.blit(
                sprite.image,
                sprite.rect.topleft - camera.offset
            )
    print("main BOOT OK")
    pygame.init()
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    #top left Icon GMH
    pygame.display.set_icon(icon)


    await src.menu.show_menu(screen, screen_width, screen_height)

    bgBig = pygame.transform.scale(bg, (bg.get_size()[0] * 2, bg.get_size()[1] * 2)).convert()
    world_width, world_height = bgBig.get_size()
    print(world_width, world_height)

    #mini_map

    minimap_surface,minimap_pos,SCALE_X,SCALE_Y = src.mini_map.create_minimap(world_width,world_height,screen_width)
    
    pygame.display.set_caption("No Lock, No Mercy")
    clock = pygame.time.Clock()
    sound = SoundManager()




    running = True
    colliding_Bike = None
    picked_up_bike = None

    camera = Camera(screen_width, screen_height)
    player = Player(100, 900)
    possible_bike_positions = []
    possible_cop_positions = []
    police = []
    obstacles = [Bike(200, 900, 90, 60, color=(0, 255, 0), transparency=150, passthrough=True)]

    #score bored GMH
    score = 0
    pygame.font.init()
    score_font = pygame.font.SysFont("consolas", 24)
    scoreBored_img = pygame.image.load(scoreBored_Path).convert_alpha()
    scoreBored_img = pygame.transform.scale(scoreBored_img,(150,150))
   

    sprites = pygame.sprite.Group(player, *obstacles, *police, )
    hitbox_objects = Hitbox.load_map_objects('assets/images/hitbox_map.png')

    print(len(hitbox_objects))
    for obj in hitbox_objects:
        if obj['type'] == 'house' or obj['type'] == 'water':
            obstacle = Obstacle(
                obj['rect'].x,
                obj['rect'].y,
                obj['rect'].width,
                obj['rect'].height,
                obstacle_type=obj['type'],
                transparency=0,
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

    amount_of_cops = 10
    min_distance_between_cops = 400

    selected_cops_positions = []

    if possible_cop_positions:

        random.shuffle(possible_cop_positions)
        # cop_positions = random.sample(possible_cop_positions, min(amount_of_cops, len(possible_cop_positions)))
        for pos in possible_cop_positions:
            # new_cop = Police(pos[0], pos[1], hitbox_objects)
            # police.append(new_cop)
            # print("police:", pos)
            if len(selected_cops_positions) >= amount_of_cops:
                break

            is_far_enough = True
            for selected_pos in selected_cops_positions:
                dist = math.hypot(pos[0] - selected_pos[0], pos[1] - selected_pos[1])

                if dist < min_distance_between_cops:
                    is_far_enough = False
                    break

            if is_far_enough:
                selected_cops_positions.append(pos)

        for pos in selected_cops_positions:
            new_cop = Police(pos[0], pos[1], hitbox_objects)
        cop_positions = random.sample(possible_cop_positions, min(amount_of_cops, len(possible_cop_positions)))
        for pos in cop_positions:
            new_cop = Police(pos[0], pos[1], hitbox_objects, spawn_pos=pos)
            police.append(new_cop)

    # sprites = pygame.sprite.Group(player, obstacles, police)
    sprites = pygame.sprite.Group(player, *obstacles, *police)

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
                        sound.play_sound("bike_throw")
                        print("You threw the bike in the water.")
                        player.image = player.image_normal
                        picked_up_bike = None
                        score += 100
                        player.start_throw_animation()
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


        keys = pygame.key.get_pressed()

        old_pos_player = player.get_position()
        player.update(keys, picked_up_bike)
        desired_pos_player = player.get_position()

        camera.follow(player)
        screen.fill((255, 255, 255))

        if picked_up_bike:
            sound.stop_sound("background")
            sound.play_sound("chase")
            for p in police:
                p.set_speed(3)
                p.update(player.get_rect())
        else:
            sound.stop_sound("chase")
            sound.play_sound("background")

        # for obstacle in obstacles:
        #     if obstacle.collides_with(player.rect):
        #
        #         if not obstacle.is_passthrough():
        #             player.set_position(old_pos_player)
        #
        #         if obstacle.is_bike():
        #             current_colliding_bike = obstacle
        player.set_position(old_pos_player)
        player.set_position((desired_pos_player[0], old_pos_player[1]))

        current_colliding_bike = None
        for obstacle in obstacles:
            if obstacle.collides_with(player.rect):
                if not obstacle.is_passthrough():

                    if player.rect.centerx > obstacle.rect.centerx:
                        player.rect.left = obstacle.rect.right
                    else:
                        player.rect.right = obstacle.rect.left
                if obstacle.is_bike():
                    current_colliding_bike = obstacle

        resolved_x, _ = player.get_position()
        player.set_position((resolved_x, desired_pos_player[1]))

        for obstacle in obstacles:
            if obstacle.collides_with(player.rect):
                if not obstacle.is_passthrough():

                    if player.rect.centery > obstacle.rect.centery:
                        player.rect.top = obstacle.rect.bottom
                    else:
                        player.rect.bottom = obstacle.rect.top
                if obstacle.is_bike():
                    current_colliding_bike = obstacle


        colliding_Bike = current_colliding_bike

        if picked_up_bike:
            for p in police:
                p.update(player.get_rect())
                if p.rect.colliderect(player.rect):
                    sound.stop_sound("chase")
                    sound.play_sound("game_over")
                    result = await src.end_screen.show_end_screen(screen, screen_width, screen_height)
                    if result == "restart":
                        await main()
                    return
        else:
            for p in police:
                p.idle()

        # mini_map
        draw(screen, camera, sprites, bgBig, bgBig.get_rect())

        # draw score UI
        score_text = score_font.render(f"    {score}", True, (255, 255, 255))
        screen.blit(score_text, (50, 20))
        screen.blit(scoreBored_img, (10, 10))
         # draw minimap on top
        src.mini_map.draw_minimap(
            minimap_surface,
            minimap_pos,
            SCALE_X,
            SCALE_Y,
            screen,
            player,
            obstacles,
            police,
            camera
        )

        # player out of bounds
        if player.rect.left < 0 or player.rect.right > world_width or player.rect.top < 0 or player.rect.bottom > world_height:
            player.set_position(old_pos_player)

       
        #draw score gmh
        score_text = score_font.render(f"    {score}",True,(255,255,255))
        screen.blit(score_text,(50,20))
        screen.blit(scoreBored_img,(10,10))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()


    #main()
asyncio.run(main())
    #asyncio.run(main())

    
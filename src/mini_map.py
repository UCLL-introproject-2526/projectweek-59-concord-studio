import pygame

MINIMAP_WIDTH = 200

def draw_map(world_height,world_width,screen_width):

   

    MINIMAP_HEIGHT = int(world_height * (MINIMAP_WIDTH / world_width))
    SCALE_X = MINIMAP_WIDTH / world_width
    SCALE_Y = MINIMAP_HEIGHT / world_height

    minimap_surface = pygame.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT))
    minimap_pos = (screen_width - MINIMAP_WIDTH - 10, 10)  # top-right


# #mini_map gmh
        
#         minimap_surface.fill((10, 10, 10))  # dark background
#         #minimap_surface = pygame.image.load('../assets/images/mini_map.png').convert()

#         #player (blue)
#         px = int(player.rect.centerx * SCALE_X)
#         py = int(player.rect.centery * SCALE_Y)
#         pygame.draw.circle(minimap_surface, (0, 0, 255), (px, py), 3)

#         #bikes (green)
#         for obs in obstacles:
#             if hasattr(obs, "is_bike") and obs.is_bike():
#                bx = int(obs.rect.centerx * SCALE_X)
#                by = int(obs.rect.centery * SCALE_Y)
#                pygame.draw.rect(minimap_surface, (0, 255, 0), (bx - 2, by - 2, 4, 4))

#         # cops (red)
#         for cop in police:
#             cx = int(cop.rect.centerx * SCALE_X)
#             cy = int(cop.rect.centery * SCALE_Y)
#             pygame.draw.circle(minimap_surface, (255, 0, 0), (cx, cy), 3)

#         # camera view rectangle (like the article’s white rect)
#         # camera.offset is the top-left of the current view in world coords
#         view_x = int(camera.offset.x * SCALE_X)
#         view_y = int(camera.offset.y * SCALE_Y)
#         view_w = int(screen_width * SCALE_X)
#         view_h = int(screen_height * SCALE_Y)
#         pygame.draw.rect(minimap_surface, (255, 255, 255), (view_x, view_y, view_w, view_h), 1)

#         # border + blit
#         pygame.draw.rect(minimap_surface, (255, 255, 255), minimap_surface.get_rect(), 1)
#         screen.blit(minimap_surface, minimap_pos)

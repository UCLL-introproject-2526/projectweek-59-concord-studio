# minimap.py
import pygame

MINIMAP_WIDTH = 200

def create_minimap(world_width, world_height, screen_width):
    minimap_height = int(world_height * (MINIMAP_WIDTH / world_width))
    scale_x = MINIMAP_WIDTH / world_width
    scale_y = minimap_height / world_height

    surface = pygame.Surface((MINIMAP_WIDTH, minimap_height))
    pos = (screen_width - MINIMAP_WIDTH - 10, 10)

    return surface, pos, scale_x, scale_y

def draw_minimap(surface, pos, scale_x, scale_y, screen,
                 player, obstacles, police, camera):
    surface.fill((10, 10, 10))  # background

    # player
    px = int(player.rect.centerx * scale_x)
    py = int(player.rect.centery * scale_y)
    pygame.draw.circle(surface, (0, 0, 255), (px, py), 3)

    # bikes
    for obs in obstacles:
        if hasattr(obs, "is_bike") and obs.is_bike():
            bx = int(obs.rect.centerx * scale_x)
            by = int(obs.rect.centery * scale_y)
            pygame.draw.rect(surface, (0, 255, 0), (bx - 2, by - 2, 4, 4))

    # cops
    for cop in police:
        cx = int(cop.rect.centerx * scale_x)
        cy = int(cop.rect.centery * scale_y)
        pygame.draw.circle(surface, (255, 0, 0), (cx, cy), 3)

    # camera rectangle
    view_x = int(camera.offset.x * scale_x)
    view_y = int(camera.offset.y * scale_y)
    view_w = int(screen.get_width() * scale_x)
    view_h = int(screen.get_height() * scale_y)
    pygame.draw.rect(surface, (255, 255, 255), (view_x, view_y, view_w, view_h), 1)

    # border and blit
    pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 1)
    screen.blit(surface, pos)

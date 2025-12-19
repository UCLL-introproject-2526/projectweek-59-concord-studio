import pygame
import sys
import asyncio
from src.soundmanager import SoundManager

sound = SoundManager()

WIN_BACKGROUND = 'assets/images/win_screen.png'
MENU_NORMAL_IMAGE = 'assets/images/return_to_menu.png'     
MENU_HOVER_IMAGE = 'assets/images/return_to_menu_selected.png'

TARGET_WIDTH = 230
TARGET_HEIGHT = 210
COLLISION_SHRINK_Y = 70

async def show_win_screen(screen, width, height):
    pygame.font.init()

    try:
        bg = pygame.image.load(WIN_BACKGROUND).convert()
        bg = pygame.transform.scale(bg, (width, height))
        
        btn_normal = pygame.transform.scale(pygame.image.load(MENU_NORMAL_IMAGE).convert_alpha(), (TARGET_WIDTH, TARGET_HEIGHT))
        btn_hover = pygame.transform.scale(pygame.image.load(MENU_HOVER_IMAGE).convert_alpha(), (TARGET_WIDTH, TARGET_HEIGHT))
    except pygame.error as e:
        print(f"Error loading win screen images: {e}")
        return "menu"

    rect_height = TARGET_HEIGHT - (2 * COLLISION_SHRINK_Y)
    button_rect = pygame.Rect(0, 0, TARGET_WIDTH, rect_height)
    button_rect.center = (width // 2, height // 2 + 100) 

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        is_hovering = button_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and is_hovering:
                    return "menu"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "menu"

        screen.blit(bg, (0, 0))

        draw_x = button_rect.left
        draw_y = button_rect.top - COLLISION_SHRINK_Y

        if is_hovering:
            screen.blit(btn_hover, (draw_x, draw_y))
        else:
            screen.blit(btn_normal, (draw_x, draw_y))

        pygame.display.flip()
        await asyncio.sleep(0)
    sound.stop_sound("background")

import pygame
import sys
from src.soundmanager import SoundManager

BACKGROUND_IMAGE = 'assets/images/game_over_screen.png'
RESTART_NORMAL = 'assets/images/try_again.png'
RESTART_HOVER = 'assets/images/try_again_selected.png'

TARGET_WIDTH = 200
TARGET_HEIGHT = 180
COLLISION_SHRINK_Y = 15
Y_OFFSET = 170

def show_end_screen(screen, width, height):
    try:
        restart_n = pygame.transform.scale(pygame.image.load(RESTART_NORMAL).convert_alpha(), (TARGET_WIDTH, TARGET_HEIGHT))
        restart_h = pygame.transform.scale(pygame.image.load(RESTART_HOVER).convert_alpha(), (TARGET_WIDTH, TARGET_HEIGHT))
        
        background = pygame.image.load(BACKGROUND_IMAGE).convert()
        background = pygame.transform.scale(background, (width, height))
    except pygame.error as e:
        print(f"Error loading end screen images: {e}")
        return

    rect_height = TARGET_HEIGHT - (2 * COLLISION_SHRINK_Y)
    
    menu_options = [
        {
            "label": "Restart",
            "normal": restart_n,
            "hover": restart_h,
            "rect": pygame.Rect(0, 0, TARGET_WIDTH, rect_height),
            "action": "restart"
        }
    ]

    for opt in menu_options:
        opt["rect"].center = (width // 2, height // 2 + Y_OFFSET)

    selected = 0
    sound = SoundManager()
    sound.play_sound("menu_music") 
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    sound.stop_sound("menu_music")
                    return "restart"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu_options[0]["rect"].collidepoint(event.pos):
                        sound.stop_sound("menu_music")
                        return "restart"

        screen.blit(background, (0, 0))

        opt = menu_options[0]
        draw_x = opt["rect"].left
        draw_y = opt["rect"].top - COLLISION_SHRINK_Y
        
        if opt["rect"].collidepoint(mouse_pos):
            screen.blit(opt["hover"], (draw_x, draw_y))
        else:
            screen.blit(opt["normal"], (draw_x, draw_y))

        pygame.display.flip()
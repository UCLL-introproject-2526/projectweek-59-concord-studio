import pygame
import sys
from soundmanager import SoundManager


BACKGROUND_IMAGE = '../assets/images/main_menu.png'

PLAY_NORMAL_IMAGE = '../assets/images/play.png'
PLAY_HOVER_IMAGE = '../assets/images/play_selected.png'
CREDITS_NORMAL_IMAGE = '../assets/images/credits.png'
CREDITS_HOVER_IMAGE = '../assets/images/credits_selected.png'
QUIT_NORMAL_IMAGE = '../assets/images/quit.png'
QUIT_HOVER_IMAGE = '../assets/images/quit_selected.png'

TARGET_WIDTH = 230
TARGET_HEIGHT = 210
COLLISION_SHRINK_Y = 70
VERTICAL_GAP = 70
Y_OFFSET = 160

def show_menu(screen, width, height):
    pygame.font.init() 

    try:
        play_normal = pygame.transform.scale(pygame.image.load(PLAY_NORMAL_IMAGE).convert_alpha(), (TARGET_WIDTH, TARGET_HEIGHT))
        play_hover = pygame.transform.scale(pygame.image.load(PLAY_HOVER_IMAGE).convert_alpha(), (TARGET_WIDTH, TARGET_HEIGHT))
        credits_normal = pygame.transform.scale(pygame.image.load(CREDITS_NORMAL_IMAGE).convert_alpha(), (TARGET_WIDTH, TARGET_HEIGHT))
        credits_hover = pygame.transform.scale(pygame.image.load(CREDITS_HOVER_IMAGE).convert_alpha(), (TARGET_WIDTH, TARGET_HEIGHT))
        quit_normal = pygame.transform.scale(pygame.image.load(QUIT_NORMAL_IMAGE).convert_alpha(), (TARGET_WIDTH, TARGET_HEIGHT))
        quit_hover = pygame.transform.scale(pygame.image.load(QUIT_HOVER_IMAGE).convert_alpha(), (TARGET_WIDTH, TARGET_HEIGHT))

        background = pygame.image.load(BACKGROUND_IMAGE).convert()
        background = pygame.transform.scale(background, (width, height))
    except pygame.error as e:
        print(f"--- IMAGE LOADING ERROR ---")
        print(f"Error loading an image: {e}")
        raise
    
    rect_height = TARGET_HEIGHT - (2 * COLLISION_SHRINK_Y)

    if rect_height <= 0:
        print("ERROR: COLLISION_SHRINK_Y is too large! Check TARGET_HEIGHT and COLLISION_SHRINK_Y values.")
        return
    options = ["Play", "Quit"]

    base_rect = play_normal.get_rect()

    menu_options = [
        {
            "name": "Play",
            "normal_img": play_normal,
            "hover_img": play_hover,
            "rect": pygame.Rect(
                base_rect.left, 
                base_rect.top, 
                TARGET_WIDTH, 
                rect_height
            ),
            "action": "play"
        },
        {
            "name": "Credits",
            "normal_img": credits_normal,
            "hover_img": credits_hover,
            "rect": pygame.Rect(
                base_rect.left, 
                base_rect.top, 
                TARGET_WIDTH, 
                rect_height
            ),
            "action": "credits"
        },
        {
            "name": "Quit",
            "normal_img": quit_normal,
            "hover_img": quit_hover,
            "rect": pygame.Rect(
                base_rect.left, 
                base_rect.top, 
                TARGET_WIDTH, 
                rect_height
            ),
            "action": "quit"
        }
    ]

    play_y = height // 2 - (len(menu_options) - 1) * VERTICAL_GAP // 2 + Y_OFFSET

    for i, option in enumerate(menu_options):
        option["rect"].center = (
            width // 2,
            play_y + i * VERTICAL_GAP
        )
        
    selected = 0

    running = True
    sound = SoundManager()
    sound.play_sound("menu_music") 
    while running:
        
        

        mouse_pos = pygame.mouse.get_pos()

        mouse_hover_index = -1

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1: 
                    for i, option in enumerate(menu_options):
                        if option["rect"].collidepoint(e.pos):
                            if option["action"] == "play":
                                sound.stop_sound("menu_music")
                                return
                            elif option["action"] == "credit":
                                pass
                            elif option["action"] == "quit":
                                pygame.quit(); sys.exit()
            
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_options)
                elif e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_options)
                elif e.key == pygame.K_RETURN:
                    option_to_act_on = menu_options[selected]
                    if option_to_act_on["action"] == "play":
                        sound.stop_sound("menu_music")
                        return
                    if option_to_act_on["action"] == "credit":
                        pass
                    elif option_to_act_on["action"] == "quit":
                        pygame.quit(); sys.exit()

        screen.blit(background, (0, 0))

        draw_y = option["rect"].top - COLLISION_SHRINK_Y
        draw_x = option["rect"].left 

        for i, option in enumerate(menu_options):
            draw_y = option["rect"].top - COLLISION_SHRINK_Y
            draw_x = option["rect"].left 

            if option["rect"].collidepoint(mouse_pos):
                mouse_hover_index = i
            
            if mouse_hover_index == i or selected == i:
                screen.blit(option["hover_img"], (draw_x, draw_y))
                if mouse_hover_index == i:
                    selected = i
            else:
                screen.blit(option["normal_img"], (draw_x, draw_y))
        
        pygame.display.flip()








# import pygame
# import sys

# def show_menu(screen, width, height):
#     pygame.font.init()
#     # font = pygame.font.get_sdl_ttf_version("Arial.ttf")
#     font = pygame.font.SysFont(None, 40)
#     options = ["Start", "Quit"]
#     selected = 0

#     while True:
#         screen.fill((0, 0, 0))

#         for i, option in enumerate(options):
#             color = (255, 255, 0) if i == selected else (255, 255, 255)
#             text = font.render(option, True, color)
#             screen.blit(text, (width // 2 - text.get_width() // 2, height //  2 + i * 60))
        
#         pygame.display.flip()

#         for e in pygame.event.get():
#             if e.type == pygame.QUIT:
#                 pygame.quit(); sys.exit()
#             if e.type == pygame.KEYDOWN:
#                 if e.key == pygame.K_UP:
#                     selected = (selected - 1) % len(options)
#                 elif e.key == pygame.K_DOWN:
#                     selected = (selected + 1) % len(options)
#                 elif e.key == pygame.K_RETURN:
#                     if options[selected] == "Start":
#                         return
#                     else:
#                         pygame.quit(); sys.exit()
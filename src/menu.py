import pygame
import sys

def show_menu(screen, width, height):
    pygame.font.init()
    # font = pygame.font.get_sdl_ttf_version("Arial.ttf")
    font = pygame.font.SysFont(None, 40)
    options = ["Start", "Quit"]
    selected = 0

    while True:
        screen.fill((0, 0, 0))

        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            text = font.render(option, True, color)
            screen.blit(text, (width // 2 - text.get_width() // 2, height //  2 + i * 60))
        
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif e.key == pygame.K_RETURN:
                    if options[selected] == "Start":
                        return
                    else:
                        pygame.quit(); sys.exit()








# font = pygame.font.SysFont("Arial", 40)
# screen_width = 800
# screen_height = 600
# screen = pygame.display.set_mode((screen_width, screen_height))

# def draw_text(text, font, color, surface, x, y):
#     textobj = font.render(text, 1, color)
#     textrect = textobj.get_rect()
#     textrect.topleft = (x, y)
#     surface.blit(textobj, textrect)

# click = False

# def main_menu():
#     pygame.display.set_caption("Menu")

#     while True:

#         screen.blit("../assets/main_menu.png")
#         draw_text('main menu', font, (255, 255 ,255), screen, 20, 20)

#         mx, my = pygame.mouse.get_pos()

#         button_1 = pygame.Rect(50, 100, 200, 50)
#         button_2 = pygame.Rect(50, 200, 200, 50)
#         if button_1.collidepoint((mx, my)):
#             if click:
#                 game()
#         if button_2.collidepoint((mx, my)):
#             if click:
#                 pass
#         pygame.draw.rect(screen, (255, 0, 0), button_1)
#         pygame.draw.rect(screen, (255, 0, 0), button_2)

#         click = False
#         for event in  pygame.event.get():
#             if event.type == quit:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     pygame.quit()
#                     sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     click = True
        
#         pygame.display.update()

# def game():
#     running = True
#     while running:
#         screen((0, 0, 0))
#         draw_text('game', font, (255, 255 ,255), screen, 20, 20)
#         for event in  pygame.event.get():
#             if event.type == quit:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     pygame.quit()
#                     sys.exit()
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     running = False
#         pygame.display.update()
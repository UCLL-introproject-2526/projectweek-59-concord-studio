import pygame
import asyncio

async def show_win_screen(screen, screen_width, screen_height):
    try:
        win_bg = pygame.image.load('assets/images/win_screen.png').convert()
        win_bg = pygame.transform.scale(win_bg, (screen_width, screen_height))
    except:
        win_bg = pygame.Surface((screen_width, screen_height))
        win_bg.fill((0, 150, 0)) 

    font = pygame.font.SysFont("consolas", 32)
    button_text = font.render("RETURN TO MAIN MENU", True, (255, 255, 255))
    
    button_rect = button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

    running = True
    while running:
        # sound.play_sound("win")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return "menu"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "menu"

        screen.blit(win_bg, (0, 0))
        
        pygame.draw.rect(screen, (0, 0, 0), button_rect.inflate(20, 20))
        screen.blit(button_text, button_rect)

        pygame.display.flip()
        await asyncio.sleep(0)
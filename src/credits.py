import pygame
import sys
from src.soundmanager import SoundManager 
import asyncio

sound = SoundManager()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCROLL_SPEED = 1.5
FONT_SIZE = 36
LINE_SPACING = 40 
IMAGE_WIDTH = 150 

CREDITS_DATA = [
    "IMG:assets/images/LogoName.png",
    "IMG:assets/images/credits_jail.png" 
    "",
    "--- DEVELOPERS ---",
    "IMG:assets/images/Adan_8bit.png",
    "ADAN FLORES",
    "IMG:assets/images/Aidan_8bit.png",
    "AIDAN COSSU",
    "IMG:assets/images/Gavin_8bit.png",
    "GAVIN MCHUGH",
    "IMG:assets/images/Noah_8bit.png",
    "NOAH COSSU",
    "IMG:assets/images/Vedat_8bit.png",
    "VEDAT CINGOZ",
    "--- BACKGROUND ---",
    "ADAN FLORES",
    "--- SPRITES ---",
    "CHARLES GEORGE PETER TWINNINGS",
    "GEMINIAIA GOOGLINGS",
    "",
    "--- SPECIAL THANKS ---",
    "TO RAZA FOR NOT PUSHING\nAND BREAKING THE GAME!",
    "",
    "A Concord Studios game",
    "IMG:assets/images/concord_8bit.png",
    "THANKS FOR PLAYING!"
]

async def show_credits(screen, width, height):
    clock = pygame.time.Clock()
    
    font_path = "assets/Perfect_DOS_VGA_437.ttf" 
    
    try:
        font = pygame.font.Font(font_path, 36)
        title_font = pygame.font.Font(font_path, 60) 
    except:
        print(f"Could not find font at {font_path}, using default.")
        font = pygame.font.SysFont("Arial", 36)
        title_font = pygame.font.SysFont("Arial", 60)
    
    loaded_assets = []
    current_y_offset = 0

    for item in CREDITS_DATA:
        if not item.startswith("IMG:"):
            if item == "NO LOCK, NO MERCY": 
                asset_surface = title_font.render(item, True, WHITE)
            else:
                asset_surface = font.render(item, True, WHITE)

        asset_surface = None
        item_height = 0

        if item.startswith("IMG:"):
            image_path = item.split("IMG:")[1]
            try:
                img = pygame.image.load(image_path).convert_alpha()
                
                aspect_ratio = img.get_height() / img.get_width()
                target_height = int(IMAGE_WIDTH * aspect_ratio)
                img = pygame.transform.scale(img, (IMAGE_WIDTH, target_height))
                
                asset_surface = img
                item_height = target_height
            except Exception as e:
                print(f"Error loading credit image '{image_path}': {e}")
                asset_surface = pygame.Surface((IMAGE_WIDTH, IMAGE_WIDTH))
                asset_surface.fill((255, 0, 0))
                item_height = IMAGE_WIDTH
        else:
            if item.strip() == "":
                 asset_surface = None
                 item_height = FONT_SIZE // 2 
            else:
                 asset_surface = font.render(item, True, WHITE)
                 item_height = asset_surface.get_height()

        if asset_surface:
            loaded_assets.append({
                'surf': asset_surface,
                'y_rel': current_y_offset,
                'height': item_height
            })
        
        current_y_offset += item_height + LINE_SPACING

    total_content_height = current_y_offset
    
    scroll_y = height 
    
    waiting = False
    wait_start_time = 0
    
    running = True
    while running:
        sound.play_sound("credits")
        screen.fill(BLACK) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    sound.stop_sound("credits")
                    return

        if not waiting:
            scroll_y -= SCROLL_SPEED
            current_bottom_pos = scroll_y + total_content_height

            if current_bottom_pos < height // 2 + 100: 
                waiting = True
                wait_start_time = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - wait_start_time > 5000:
                sound.stop_sound("credits")
                return

        for asset in loaded_assets:
            draw_y = scroll_y + asset['y_rel']
            
            if -asset['height'] < draw_y < height:
                rect = asset['surf'].get_rect(center=(width // 2, draw_y + asset['height'] // 2))
                screen.blit(asset['surf'], rect)

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

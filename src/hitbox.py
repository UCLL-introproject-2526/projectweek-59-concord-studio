import pygame
import os

class Hitbox:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    TILE_SIZE = 32 
    
    COLOR_MAP = {
        (255, 0, 0): 'house',
        (0, 0, 255): 'water',
        (255, 255, 255): 'background'
    }
    OBSTACLE_TYPES = ['house', 'water']

    @staticmethod
    def load_map_objects(image_path):
        game_objects = []
        
        try:
            map_image = pygame.image.load(image_path).convert() 
        except pygame.error as e:
            print(f"Error loading map image: {e}")
            print(f"Pygame failed to load image at: {image_path}")
            return [] 
    
        width, height = map_image.get_size()

        for x in range(0, width, Hitbox.TILE_SIZE):
            for y in range(0, height, Hitbox.TILE_SIZE):
                
                pixel_color = map_image.get_at((x, y))[:3]

                hitbox_type = Hitbox.COLOR_MAP.get(pixel_color)

                if hitbox_type and hitbox_type in Hitbox.OBSTACLE_TYPES:
                    
                    hitbox_rect = pygame.Rect(x, y, Hitbox.TILE_SIZE, Hitbox.TILE_SIZE)
                    
                    game_objects.append({
                        'type': hitbox_type,
                        'rect': hitbox_rect,
                        'color': pixel_color
                    })
                    
        return game_objects
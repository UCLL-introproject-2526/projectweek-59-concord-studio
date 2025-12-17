import pygame
import os

class Hitbox:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    TILE_SIZE = 32 
    SCALE_FACTOR = 2  
    
    COLOR_MAP = {
        (255, 2, 2): 'house',
        (0, 52, 253): 'water',
        (255, 255, 255): 'background',
        (255, 220, 2): 'bike-spawn',
        (255, 0, 248): 'cop'
    }
    OBSTACLE_TYPES = ['house', 'water', 'bike-spawn', 'cop']

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
        
        SCALED_TILE_SIZE = Hitbox.TILE_SIZE * Hitbox.SCALE_FACTOR

        for x in range(0, width, Hitbox.TILE_SIZE):
            for y in range(0, height, Hitbox.TILE_SIZE):
                
                pixel_color = map_image.get_at((x, y))[:3]
                hitbox_type = Hitbox.COLOR_MAP.get(pixel_color)

                if hitbox_type and hitbox_type in Hitbox.OBSTACLE_TYPES:
                    
                    scaled_x = x * Hitbox.SCALE_FACTOR
                    scaled_y = y * Hitbox.SCALE_FACTOR
                    
                    hitbox_rect = pygame.Rect(
                        scaled_x, 
                        scaled_y, 
                        SCALED_TILE_SIZE,  
                        SCALED_TILE_SIZE   
                    )
                    
                    game_objects.append({
                        'type': hitbox_type,
                        'rect': hitbox_rect,
                        'color': pixel_color
                    })
                    
        return game_objects
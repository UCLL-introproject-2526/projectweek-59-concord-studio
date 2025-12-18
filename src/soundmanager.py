import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=4, buffer=4096)
        self.sounds = {
            "chase": pygame.mixer.Sound("assets/sfx/chase.ogg"),
            "bike_throw": pygame.mixer.Sound("assets/sfx/bike_throw.ogg"),
            "background": pygame.mixer.Sound("assets/sfx/ambient_music.ogg"), #added
            "start_up_sfx": pygame.mixer.Sound("assets/sfx/game_start_up.ogg"),
            "menu_music": pygame.mixer.Sound("assets/sfx/menu_music.ogg"), #added
            "game_over": pygame.mixer.Sound("assets/sfx/game_over.ogg"), #added
            "credits": pygame.mixer.Sound("assets/sfx/credits.ogg")

        }

    def play_sound(self, sound_name, volume=1, loops=0):
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(volume)
            self.sounds[sound_name].play(loops)

    def stop_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
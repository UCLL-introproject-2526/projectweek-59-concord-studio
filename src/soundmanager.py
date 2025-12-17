import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "chase": pygame.mixer.Sound("../sfx/audio cop chase.wav"),
            "bike_throw": pygame.mixer.Sound("../sfx/bike throw.wav"),
            "background": pygame.mixer.Sound("../sfx/ingame ambient music.wav"), #added
            "start_up_sfx": pygame.mixer.Sound("../sfx/game start up.wav"),
            "menu_music": pygame.mixer.Sound("../sfx/menu music.wav"), #added
            "game_over": pygame.mixer.Sound("../sfx/game over.wav") #added

        }

    def play_sound(self, sound_name, volume=1, loops=0):
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(volume)
            self.sounds[sound_name].play(loops)

    def stop_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
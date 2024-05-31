import pygame
import pygame.mixer
pygame.mixer.init()

attack_sound = pygame.mixer.Sound('assets/audio/attack.wav')
click_sound = pygame.mixer.Sound('assets/audio/click.wav')
damage_sound = pygame.mixer.Sound('assets/audio/damage.wav')
drop_sound = pygame.mixer.Sound('assets/audio/drop.wav')
jump_sound = pygame.mixer.Sound('assets/audio/jump.wav')

jump_sound.set_volume(0.4)
attack_sound.set_volume(0.7)
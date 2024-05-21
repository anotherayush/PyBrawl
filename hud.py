import pygame
from settings import *

class HUD:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)

    def draw(self, screen):
        health_text = self.font.render(f'Health: {self.player.hp}', True, WHITE)
        screen.blit(health_text, (10, 10))

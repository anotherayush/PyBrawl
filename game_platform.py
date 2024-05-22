import pygame
from settings import *
from random import randint

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class PlatformSelector:
    def __init__(self):
        self.selected_platform = 1

    def draw(self, screen):
        screen.fill(BLACK)
        font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        text = font.render("Select Platform (1, 2, 3, or 4)", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(text, text_rect)

        text = font.render(f"Selected: {self.selected_platform}", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(text, text_rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.selected_platform = 1
                elif event.key == pygame.K_2:
                    self.selected_platform = 2
                elif event.key == pygame.K_3:
                    self.selected_platform = 3
                elif event.key == pygame.K_4:
                    self.selected_platform = 4
    
    def get_selected_platform(self):
        return self.selected_platform

    def create_platforms(self, selected_platform):
        if selected_platform == 1:
            platforms = [
                Platform(100, 400, 300, 25),
                Platform(500, 300, 200, 25),
                Platform(700, 200, 250, 25)
            ]
        elif selected_platform == 2:
            platforms = [
                Platform(40, 200, 350, 25),
                Platform(250, 450, 400, 25),
                Platform(600, 300, 350, 25)
]
        elif selected_platform == 3:
            platforms = [
                Platform(100, 400, 250, 25),
                Platform(450, 330, 300, 25),
                Platform(250, 200, 200, 25)
            ]
        elif selected_platform == 4:
            platforms = [
                Platform(600, 450, 400, 25),
                Platform(300, 350, 250, 25),
                Platform(50, 250, 300, 25)
            ]
        else:
            platforms = []

        return platforms

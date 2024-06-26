import pygame
from settings import *
from sounds import click_sound

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.background = pygame.image.load("assets/art/back.png").convert()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class PlatformSelector:
    def __init__(self):
        self.selected_platform = 1
        self.background = pygame.image.load("assets/art/back.png").convert()

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
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
                    click_sound.play()
                elif event.key == pygame.K_2:
                    self.selected_platform = 2
                    click_sound.play()
                elif event.key == pygame.K_3:
                    self.selected_platform = 3
                    click_sound.play()
                elif event.key == pygame.K_4:
                    self.selected_platform = 4
                    click_sound.play()
    
    def get_selected_platform(self):
        return self.selected_platform

    def create_platforms(self, selected_platform):
        platforms = []

        if selected_platform == 1:
            for x in range(100, 400, 25):
                platforms.append(Platform(x, 400, 25, 25, "assets/art/platform.png"))
            for x in range(500, 700, 25):
                platforms.append(Platform(x, 300, 25, 25, "assets/art/platform.png"))
            for x in range(700, 950, 25):
                platforms.append(Platform(x, 200, 25, 25, "assets/art/platform.png"))
        elif selected_platform == 2:
            for x in range(80, 430, 25):
                platforms.append(Platform(x, 280, 25, 25, "assets/art/platform.png"))
            for x in range(250, 650, 25): 
                platforms.append(Platform(x, 450, 25, 25, "assets/art/platform.png"))
            for x in range(580, 930, 25):
                platforms.append(Platform(x, 330, 25, 25, "assets/art/platform.png"))
        elif selected_platform == 3:
            for x in range(100, 400, 25):
                platforms.append(Platform(x, 400, 25, 25, "assets/art/platform.png"))
            for x in range(450, 750, 25): 
                platforms.append(Platform(x, 330, 25, 25, "assets/art/platform.png"))
            for x in range(220, 420, 25): 
                platforms.append(Platform(x, 230, 25, 25, "assets/art/platform.png"))
        elif selected_platform == 4:
            for x in range(600, 1000, 25):
                platforms.append(Platform(x, 450, 25, 25, "assets/art/platform.png"))
            for x in range(300, 550, 25):
                platforms.append(Platform(x, 350, 25, 25, "assets/art/platform.png"))
            for x in range(50, 350, 25):
                platforms.append(Platform(x, 250, 25, 25, "assets/art/platform.png"))
        else:
            platforms = []

        return platforms


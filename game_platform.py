import pygame
from settings import *
from sounds import click_sound

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
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
            # Original lengths: Platform(100, 400, 300, 25)
            for x in range(100, 400, 25):  # Start at x = 100, add blocks at intervals of 25 until 400
                platforms.append(Platform(x, 400, 25, 25, "assets/art/platform.png"))
            for x in range(500, 700, 25):  # Start at x = 500, add blocks at intervals of 25 until 700
                platforms.append(Platform(x, 300, 25, 25, "assets/art/platform.png"))
            for x in range(700, 950, 25):  # Start at x = 700, add blocks at intervals of 25 until 950
                platforms.append(Platform(x, 200, 25, 25, "assets/art/platform.png"))
        elif selected_platform == 2:
            # Original lengths: Platform(80, 280, 350, 25)
            for x in range(80, 430, 25):  # Start at x = 80, add blocks at intervals of 25 until 430
                platforms.append(Platform(x, 280, 25, 25, "assets/art/platform.png"))
            for x in range(250, 650, 25):  # Start at x = 250, add blocks at intervals of 25 until 650
                platforms.append(Platform(x, 450, 25, 25, "assets/art/platform.png"))
            for x in range(580, 930, 25):  # Start at x = 580, add blocks at intervals of 25 until 930
                platforms.append(Platform(x, 330, 25, 25, "assets/art/platform.png"))
        elif selected_platform == 3:
            # Original lengths: Platform(100, 400, 300, 25)
            for x in range(100, 400, 25):  # Start at x = 100, add blocks at intervals of 25 until 400
                platforms.append(Platform(x, 400, 25, 25, "assets/art/platform.png"))
            for x in range(450, 750, 25):  # Start at x = 450, add blocks at intervals of 25 until 750
                platforms.append(Platform(x, 330, 25, 25, "assets/art/platform.png"))
            for x in range(220, 420, 25):  # Start at x = 220, add blocks at intervals of 25 until 420
                platforms.append(Platform(x, 230, 25, 25, "assets/art/platform.png"))
        elif selected_platform == 4:
            # Original lengths: Platform(600, 450, 400, 25)
            for x in range(600, 1000, 25):  # Start at x = 600, add blocks at intervals of 25 until 1000
                platforms.append(Platform(x, 450, 25, 25, "assets/art/platform.png"))
            for x in range(300, 550, 25):  # Start at x = 300, add blocks at intervals of 25 until 550
                platforms.append(Platform(x, 350, 25, 25, "assets/art/platform.png"))
            for x in range(50, 350, 25):  # Start at x = 50, add blocks at intervals of 25 until 350
                platforms.append(Platform(x, 250, 25, 25, "assets/art/platform.png"))
        else:
            platforms = []

        return platforms


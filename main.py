import pygame
import pygame.mixer
from settings import *
from game_state import GameState
from game_platform import PlatformSelector
from sounds import click_sound

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('PyBrawl')
    clock = pygame.time.Clock()
    game_state = None
    platform_selector = PlatformSelector()
    running = True
    main_screen = True
    game_running = False
    game_over = False
    platform_selection = False
    pygame.mixer.music.load('assets/audio/back.wav')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if main_screen:
                    if event.key == pygame.K_SPACE:
                        main_screen = False
                        platform_selection = True
                        click_sound.play()
                    elif event.key == pygame.K_1:
                        main_screen = False
                        game_running = True
                        game_state.reset()  # Reset game state when starting a new game
                        click_sound.play()
                elif platform_selection:
                    platform_selector.handle_events(events)
                    if event.key == pygame.K_RETURN:
                        platform_selection = False
                        game_running = True
                        selected_platform = platform_selector.get_selected_platform()
                        platforms = platform_selector.create_platforms(selected_platform)
                        game_state = GameState(platforms)  # Create GameState with selected platforms
                        game_state.reset()
                        click_sound.play()
                elif game_over:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        main_screen = True
                        game_running = False
                        game_over = False
                        game_state.reset()
                        click_sound.play()

        if main_screen:
            # Main home screen
            screen.fill(BLACK)
            font = pygame.font.Font(FONT_NAME, FONT_SIZE)
            text = font.render("Press SPACE to start", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
        elif platform_selection:
            # Platform selection screen
            platform_selector.draw(screen)
        elif game_running:
            # Game is running
            if not game_state.is_game_over():
                game_state.update()
            game_state.draw(screen)  # Draw all sprites (including platforms) using game_state.draw()
            if game_state.is_game_over():
                game_over = True
        elif game_over:
            # Game over screen
            game_state.draw_game_over(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
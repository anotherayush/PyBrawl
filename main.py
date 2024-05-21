import pygame
from settings import *
from game_state import GameState

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('PyBrawl')
    clock = pygame.time.Clock()
    game_state = GameState()
    running = True
    main_screen = True  # Flag to indicate if it's the main home screen
    game_running = False  # Flag to indicate if the game is currently running
    game_over = False  # Flag to indicate if the game is over

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if main_screen:
                    if event.key == pygame.K_SPACE:
                        main_screen = False
                        game_running = True
                        game_state.reset()  # Reset game state when starting a new game
                elif game_over:
                    if event.key == pygame.K_ESCAPE:
                        running = False  # Quit the game if ESC is pressed
                    elif event.key == pygame.K_SPACE:
                        main_screen = True
                        game_running = False
                        game_over = False  # Reset game over flag
                        game_state.reset()  # Reset game state when going back to main screen

        if main_screen:
            # Main home screen
            screen.fill(BLACK)
            font = pygame.font.Font(FONT_NAME, FONT_SIZE)
            text = font.render("Press SPACE to start", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
        elif game_running:
            # Game is running
            if not game_state.is_game_over():
                game_state.update()
                game_state.draw(screen)
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
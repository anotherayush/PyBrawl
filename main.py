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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if main_screen:
                    if event.key == pygame.K_SPACE:
                        main_screen = False
                        game_running = True
                elif game_running:
                    if event.key == pygame.K_ESCAPE:
                        main_screen = True
                        game_running = False

        if main_screen:
            # Main home screen
            screen.fill(BLUE)  # Example background color
            # Display main home screen content (e.g., title, instructions)
            # You can use pygame.draw and pygame.font to create content
            
            # Example code to display text
            font = pygame.font.Font(None, 36)
            text = font.render("Press SPACE to start", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)

        elif game_running:
            # Game is running
            game_state.update()
            game_state.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()

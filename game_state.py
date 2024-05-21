import pygame
from player import Player
from game_platform import Platform
from settings import *
import time

class GameState:
    def __init__(self):
        # Create platforms
        self.platforms = pygame.sprite.Group()
        self.platforms.add(Platform(150, 400, PLATFORM_WIDTHS[2]))
        self.platforms.add(Platform(300, 300, PLATFORM_WIDTHS[2]))
        self.platforms.add(Platform(450, 200, PLATFORM_WIDTHS[2]))

        # Create players and place them on platforms
        self.player1 = Player(175, 350, RED, {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w, 'drop': pygame.K_s, 'attack': pygame.K_SPACE}, attack_color=YELLOW, attack_damage=ATTACK_DAMAGE, max_hp=PLAYER_MAX_HP)
        self.player2 = Player(475, 250, BLUE, {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP, 'drop': pygame.K_DOWN, 'attack': pygame.K_RSHIFT}, attack_color=PURPLE, attack_damage=ATTACK_DAMAGE, max_hp=PLAYER_MAX_HP)

        self.all_sprites = pygame.sprite.Group(self.player1, self.player2, *self.platforms)
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)

        self.combo_text = ""
        self.combo_display_timer = 0

        self.game_over = False
        self.winner = None


    def update(self):
        keys = pygame.key.get_pressed()

        self.player1.update(keys)
        self.player2.update(keys)

        self.player1.update_combo_timer()
        self.player2.update_combo_timer()

        self.player1.check_collision_with_platforms(self.platforms)
        self.player2.check_collision_with_platforms(self.platforms)

        self.check_attacks()
        self.check_boundaries()
        self.check_win_conditions()
        self.check_drop_through_platforms()

        if self.game_over:
            return

        # Check win conditions
        self.check_win_conditions()

    def check_attacks(self):
        keys = pygame.key.get_pressed()

        if keys[self.player1.controls['attack']]:
            self.player1.handle_attack(self.player2, overlapping=self.player1.rect.colliderect(self.player2.rect))
        else:
            self.player1.reset_attack()

        if keys[self.player2.controls['attack']]:
            self.player2.handle_attack(self.player1, overlapping=self.player2.rect.colliderect(self.player1.rect))
        else:
            self.player2.reset_attack()

    def handle_attack(self, attacker, defender):
        damage = attacker.attack_damage
        knockback = KNOCKBACK_DISTANCE

        if attacker.combo_timer > 0:
            damage += COMBO_BONUS_DAMAGE * attacker.combo_count
            attacker.combo_count += 1
        else:
            attacker.combo_count = 1
            attacker.combo_timer = COMBO_TIMEOUT

        defender.take_damage(damage, attacker.combo_count)
        defender.rect.x += knockback if attacker.rect.x < defender.rect.x else -knockback

        attacker.combo_timer -= 1 / FPS

        if self.attack_cooldown == 0:
            overlapping = attacker.rect.colliderect(defender.rect)
            attacker.handle_attack(defender, overlapping)
        
        # Update combo count and display text
            if overlapping:
                attacker.combo_count += 1
                attacker.update_combo_text()

    def draw(self, screen):
        screen.fill(BLACK)
        self.all_sprites.draw(screen)
        self.draw_health_bars(screen)
        self.draw_hp_text(screen)
        self.player1.draw_damage_text(screen, 10, 90)  # Damage text position adjusted
        self.player2.draw_damage_text(screen, SCREEN_WIDTH - 210, 90)  # Damage text position adjusted
        self.player1.draw_combo_text(screen, SCREEN_WIDTH - 210, 120, self.player2)
        self.player2.draw_combo_text(screen, 10, 120, self.player1)
        if self.game_over:
            self.draw_game_over(screen)

    def check_boundaries(self):
        for player in [self.player1, self.player2]:
            if player.rect.left < 0:
                player.rect.left = 0
            if player.rect.right > SCREEN_WIDTH:
                player.rect.right = SCREEN_WIDTH
            if player.rect.top < 0:
                player.rect.top = 0
            if player.rect.bottom > SCREEN_HEIGHT:
                player.rect.bottom = SCREEN_HEIGHT
                player.take_damage(player.max_hp,0)  # Player loses if they fall off the screen

    def check_win_conditions(self):
        if self.player1.hp == 0:
            self.winner = "Player 2"
            self.game_over = True
        elif self.player2.hp == 0:
            self.winner = "Player 1"
            self.game_over = True


    def get_winner_text(self):
        font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        winner_text = font.render(f"{self.winner} Wins!", True, WHITE)
        return winner_text
    
    def is_game_over(self):
        return self.game_over
    
    def draw_game_over(self, screen):
        screen.fill(BLACK)
        font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        winner_text = font.render(f"{self.winner} wins!", True, WHITE)
        winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(winner_text, winner_rect)

        menu_text = font.render("Press SPACE to Start Again", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 ))
        screen.blit(menu_text, menu_rect)

        menu_text = font.render("Press ESC to Exit", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(menu_text, menu_rect)

    def draw_health_bars(self, screen):
        for player, x in [(self.player1, 10), (self.player2, SCREEN_WIDTH - 210)]:
            pygame.draw.rect(screen, RED, (x, 10, 200, 20))
            pygame.draw.rect(screen, GREEN, (x, 10, player.hp * 2, 20))
    
    def draw_hp_text(self, screen):
        player1_hp_text = self.font.render(f"HP: {self.player1.hp}", True, WHITE)
        player2_hp_text = self.font.render(f"HP: {self.player2.hp}", True, WHITE)
        combo_text_surface = self.font.render(self.combo_text, True, WHITE)
        screen.blit(player1_hp_text, (10, 40))
        screen.blit(player2_hp_text, (SCREEN_WIDTH - 210, 40))
        screen.blit(combo_text_surface, (SCREEN_WIDTH - 210, 70))

    def check_drop_through_platforms(self):
        for player in [self.player1, self.player2]:
            player.drop_through_platforms = False
    
            # Check if the player wants to drop through the current platform
            keys = pygame.key.get_pressed()
            if keys[player.controls['drop']]:
                player.drop_through_platforms = True
                player.on_ground = False
                player.can_double_jump = False

    def draw_combo_text(self, screen):
        current_time = pygame.time.get_ticks()
        if self.combo_display_timer > 0 and current_time - self.combo_display_timer < DAMAGE_TEXT_DURATION:
            combo_text_surface = self.font.render(self.combo_text, True, WHITE)
            screen.blit(combo_text_surface, (SCREEN_WIDTH - 210, 70))
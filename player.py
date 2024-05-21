import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, controls, attack_color, attack_damage, max_hp):
        super().__init__()
        self.base_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.base_image.fill(color)
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = PLAYER_SPEED
        self.jump_height = PLAYER_JUMP_HEIGHT
        self.double_jump_height = PLAYER_DOUBLE_JUMP_HEIGHT
        self.velocity_y = 0
        self.on_ground = False
        self.can_double_jump = True
        self.hp = max_hp
        self.max_hp = max_hp
        self.controls = controls
        self.attack_color = attack_color
        self.attacking = False
        self.facing_right = True
        self.damage_display_timer = 0
        self.damage_text = ""
        self.attack_damage = 10
        self.attack_cooldown = 0
        self.attack_timer = 0
        self.drop_through_platforms = False
        self.combo_count = 0
        self.combo_timer = 0
        self.combo_display_timer = 0 
        self.combo_text = ""
        self.combo_count = 0  # Initialize combo count
        self.combo_window_duration = 1000  # Combo window duration in milliseconds
        self.last_attack_time = 0  # Time of the last attack

    def update_image(self):
        self.image = pygame.transform.rotate(self.base_image, 90 if self.facing_right else -90)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center  

    def update(self, keys):
        self.velocity_y += 1  # Gravity effect
        if self.velocity_y > 10:
            self.velocity_y = 10

        if keys[self.controls['left']]:
            self.rect.x -= self.speed
            self.facing_right = False
        if keys[self.controls['right']]:
            self.rect.x += self.speed
            self.facing_right = True

        if keys[self.controls['jump']]:
            if self.on_ground:
                self.velocity_y = -self.jump_height
                self.on_ground = False
            elif self.can_double_jump:
                self.velocity_y = -self.jump_height
                self.can_double_jump = False

        self.rect.y += self.velocity_y

        # Manage attack cooldown and timer
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1

        if self.combo_timer > 0:
            self.combo_timer -= 1
        if self.combo_timer == 0:
            self.combo_count = 0

        if self.combo_count > 0:
            self.combo_text = f"COMBO X{self.combo_count}"
        else:
            self.combo_text = ""
        self.update_combo_timer()

    def check_collision_with_platforms(self, platforms):
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if self.velocity_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.can_double_jump = True
                elif self.velocity_y < 0:  # Jumping up
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

    def take_damage(self, damage, combo_count):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        self.damage_text = f"- {damage} HP"
        if combo_count > 1:
            self.combo_count = combo_count
            self.combo_timer = COMBO_DISPLAY_DURATION
        else:
            self.combo_count += 1  # Increment combo count if combo is not 1
            self.combo_timer = COMBO_DISPLAY_DURATION
        self.damage_display_timer = pygame.time.get_ticks()

    def is_opponent_in_attack_range(self, opponent):
        distance_x = abs(self.rect.x - opponent.rect.x)
        distance_y = abs(self.rect.y - opponent.rect.y)
        
        if distance_x <= ATTACK_RANGE and distance_y <= PLAYER_HEIGHT:  # Adjusted condition
            if self.facing_right and self.rect.x < opponent.rect.x:
                return True
            elif not self.facing_right and self.rect.x > opponent.rect.x:
                return True
        return False

    def draw_damage_text(self, screen, x, y):
        current_time = pygame.time.get_ticks()
        if self.damage_display_timer > 0 and current_time - self.damage_display_timer < DAMAGE_TEXT_DURATION:
            font = pygame.font.Font(FONT_NAME, FONT_SIZE)
            damage_text_surface = font.render(self.damage_text, True, WHITE)
            screen.blit(damage_text_surface, (x, y))
        else:
            self.damage_text = ""
            self.damage_display_timer = 0
    
    def handle_attack(self, opponent, overlapping=False):
        current_time = pygame.time.get_ticks()
    
        if self.attack_cooldown == 0:
            if overlapping or self.is_opponent_in_attack_range(opponent):
                self.attack(opponent)
                self.attack_timer = ATTACK_DURATION
                self.attack_cooldown = ATTACK_COOLDOWN
    
                # Check time difference since last attack
                time_difference = current_time - self.last_attack_time
    
                if time_difference <= COMBO_WINDOW_DURATION:
                    # Increment combo count if within combo window
                    self.combo_count += 1
                    self.combo_timer = COMBO_WINDOW_DURATION  # Reset combo timer when a new attack occurs within the window
                else:
                    # Reset combo count and timer if outside combo window
                    self.combo_count = 1
                    self.combo_timer = 0
    
                # Update last attack time
                self.last_attack_time = current_time
    
                # Update combo text
                self.combo_text = f"COMBO x{self.combo_count}"
                self.combo_display_timer = pygame.time.get_ticks()  # Start combo text display timer

    def attack(self, opponent):
        base_damage = 10
        combo_damage = 0
        if self.combo_count > 0:
            combo_damage = min(2, 12 - base_damage)
        total_damage = base_damage + combo_damage
        knockback = min(KNOCKBACK_DISTANCE + 2 * (self.combo_count - 1), MAX_KNOCKBACK_DISTANCE)
        
        self.combo_timer = COMBO_TIMEOUT

        # Assign total_damage directly to opponent's take_damage method
        opponent.take_damage(total_damage, self.combo_count)
        opponent.rect.x += knockback if self.rect.x < opponent.rect.x else -knockback

    def reset_attack(self):
        self.attack_timer = 0

    def check_collision_with_platforms(self, platforms):
        self.on_ground = False
        self.can_double_jump = False  # Reset double jump ability

        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if self.velocity_y > 0:  # Falling down
                    if not self.drop_through_platforms:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.on_ground = True
                        self.can_double_jump = True
                elif self.velocity_y < 0:  # Jumping up
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
    
    def update_combo_timer(self):
        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer == 0:
                self.combo_count = 0  # Reset combo count immediately after combo window expires
                self.combo_text = ""

    def update_combo_text(self, combo_count):
        if self.combo_count > 0:
            self.combo_text = f"COMBO X{self.combo_count}"
        else:
            self.combo_text = ""

    def draw_combo_text(self, screen, x, y, opponent):
        if self.combo_count > 0:  # Display combo text only when there's an active combo
            current_time = pygame.time.get_ticks()
            if self.combo_display_timer > 0 and current_time - self.combo_display_timer < DAMAGE_TEXT_DURATION:
                font = pygame.font.Font(FONT_NAME, FONT_SIZE)
                combo_text_surface = font.render(self.combo_text, True, WHITE)
                
                # Display combo text on the opponent player at the same position below the damage text
                screen.blit(combo_text_surface, (x, y))

    def reset_position(self):
    # Reset player's position to initial position
        self.rect.topleft = (self.initial_x, self.initial_y)

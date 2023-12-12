import pygame
from bullet import Bullet
import math

class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x  # X-coordinate of the player's position
        self.y = y  # Y-coordinate of the player's position
        self.width = width  # Width of the player's character
        self.height = height  # Height of the player's character
        self.color = color  # Color of the player's character
        self.rect = (x, y, width, height)  # Rectangle representing the player's character
        self.vel = 3  # Velocity/speed of the player's movement
        self.bullets = []  # List to store bullets fired by the player
        self.health = 100  # Player's health points
        self.hitbox = (self.x, self.y, self.width, self.height)  # Rectangle hitbox around the player
        self.game_over = False  # Flag indicating if the player's character is eliminated
        self.ready = False  # Flag indicating if the player is ready 
        self.victory = False # Flag indicating if player has won
        self.prev_x = x  # Store previous x-coordinate
        self.prev_y = y  # Store previous y-coordinate
        self.shoot_cooldown = 0  # Initialize the shoot cooldown timer
        self.shoot_delay = 30  # Set the delay between shots
        self.bullet_burst = False ###
        self.has_shield = False  # Flag to check if the player has a shield
        self.shield_health = 5  # Shield's health points
        self.shield_size = 45  # Radius of the shield ring
        self.shield_color = (0, 0, 255)  # Color of the shield ring
        

    def draw(self, win):
        # Draw the player's character and shield (if active) on the game window
        pygame.draw.rect(win, self.color, self.rect)
        if self.has_shield:
            shield_offset = ((self.shield_size - self.width) * 2) - (self.width/4)
            shield_rect = (
                self.x - shield_offset,
                self.y - shield_offset,
                self.width + self.shield_size,
                self.height + self.shield_size
            )
            pygame.draw.rect(win, self.shield_color, shield_rect, 2)

    def shoot(self, target_x, target_y):
        if self.shoot_cooldown == 0:
        # Create and shoot a bullet towards the target position
            bullet_speed = 3  # Set a constant bullet speed
            center_x = self.x + self.width // 2  # Calculate the center of the player character
            center_y = self.y + self.height // 2
            
            if self.bullet_burst:
                angle = math.atan2(target_y - center_y, target_x - center_x)
                
                # First bullet (straight)
                vel_x = math.cos(angle) * bullet_speed
                vel_y = math.sin(angle) * bullet_speed
                new_bullet = Bullet(center_x, center_y, vel_x, vel_y, self)
                self.bullets.append(new_bullet)

                # Second bullet (slightly up)
                angle_offset_up = 0.5  # Adjust this value to change the angle offset
                angle_up = angle + angle_offset_up
                vel_x = math.cos(angle_up) * bullet_speed
                vel_y = math.sin(angle_up) * bullet_speed
                new_bullet = Bullet(center_x, center_y, vel_x, vel_y, self)
                self.bullets.append(new_bullet)

                # Third bullet (slightly down)
                angle_offset_down = -0.5  # Adjust this value to change the angle offset
                angle_down = angle + angle_offset_down
                vel_x = math.cos(angle_down) * bullet_speed
                vel_y = math.sin(angle_down) * bullet_speed
                new_bullet = Bullet(center_x, center_y, vel_x, vel_y, self)
                self.bullets.append(new_bullet)

                self.shoot_cooldown = self.shoot_delay

            else:
                # Calculate the angle in radians towards the target
                angle = math.atan2(target_y - center_y, target_x - center_x)

                # Calculate the velocity components based on the angle and speed
                vel_x = math.cos(angle) * bullet_speed
                vel_y = math.sin(angle) * bullet_speed

                new_bullet = Bullet(center_x, center_y, vel_x, vel_y, self)
                self.bullets.append(new_bullet)
                self.shoot_cooldown = self.shoot_delay

        else:
            pass

    def hit(self):
        # Reduce the shield's health if active, else reduce player's health
        if self.has_shield:
            self.shield_health -= 1
            if self.shield_health <= 0:
                self.has_shield = False  # Deactivate shield when health drops to or below zero
        else:
            self.health -= 10
            if self.health <= 0:
                self.game_over = True  # Mark the player as eliminated if health drops to or below zero

    def activate_shield(self):
        # Activate the shield
        self.has_shield = True
        self.shield_health = 5  # Reset shield's health when activated

    def get_health(self):
        # Get the player's current health
        return self.health

    def update_hitbox(self):
        # Update the player's hitbox position and size
        if self.has_shield:
            shield_offset = ((self.shield_size - self.width) * 2) - (self.width/4)
            self.hitbox = (
                self.x - shield_offset,
                self.y - shield_offset,
                self.width + self.shield_size,
                self.height + self.shield_size
            )
        else:
            self.hitbox = (self.x, self.y, self.width, self.height)

    # Moving player and checking if they are at map border or run into a wall
    def move(self, walls):
        if not self.game_over:
            keys = pygame.key.get_pressed()

            self.prev_x, self.prev_y = self.x, self.y  # Store previous position

            if keys[pygame.K_LEFT] and self.x - self.vel > 0:
                self.x -= self.vel
                if self.check_collision(walls):
                    self.x = self.prev_x  # Revert x-coordinate

            if keys[pygame.K_RIGHT] and self.x + self.vel + self.width < 1000:
                self.x += self.vel
                if self.check_collision(walls):
                    self.x = self.prev_x  # Revert x-coordinate

            if keys[pygame.K_UP] and self.y - self.vel > 49:
                self.y -= self.vel
                if self.check_collision(walls):
                    self.y = self.prev_y  # Revert y-coordinate

            if keys[pygame.K_DOWN] and self.y + self.vel + self.height < 800:
                self.y += self.vel
                if self.check_collision(walls):
                    self.y = self.prev_y  # Revert y-coordinate

            
            self.update()
            for bullet in self.bullets[:]:
                bullet.move()
                for wall in walls:
                    if wall.rect.collidepoint((bullet.x, bullet.y)):
                        # If bullet hits a wall, remove the bullet
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break

    # Check if a player runs into a wall
    def check_collision(self, walls):
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for wall in walls:
            if player_rect.colliderect(wall.rect):
                return True
        return False

    def update(self):
        # Update the player's rectangle and hitbox positions
        self.rect = (self.x, self.y, self.width, self.height)
        self.hitbox = (self.x, self.y, self.width, self.height)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def set_ready(self):  # Set the player as ready 
        self.ready = True

    def is_ready(self):  # Check if the player is ready 
        return self.ready
    
    def reset(self):
        # Reset player attributes to their initial values
        self.health = 100  # Reset health to default value
        self.game_over = False  # Reset game_over flag
        self.ready = False  # Reset ready flag
        self.victory = False  # Reset victory flag
    
    
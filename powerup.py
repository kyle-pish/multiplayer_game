import pygame
import os

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type  # 'speed_boost', 'health_boost', etc.
        self.radius = 15 

    def draw(self, win):

        # Get the current directory of script
        current_directory = os.path.dirname(__file__)

        # Define the relative path to image file
        speed_boost_path = os.path.join(current_directory, 'assets', 'speed_boost.png')
        triple_shot_path = os.path.join(current_directory, 'assets', 'triple_shot.png')
        med_pack_path = os.path.join(current_directory, 'assets', 'med_pack.png')
        shield_path = os.path.join(current_directory, 'assets', 'shield.png')

        # Draw the loaded image onto the game window
        if self.type == 'speed_boost':
            scaled_image = pygame.transform.scale(pygame.image.load(speed_boost_path), (2 * self.radius, 2 * self.radius))
        elif self.type == 'triple_shot':
            scaled_image = pygame.transform.scale(pygame.image.load(triple_shot_path), (2 * self.radius, 2 * self.radius))
        elif self.type == 'med_pack':
            scaled_image = pygame.transform.scale(pygame.image.load(med_pack_path), (2 * self.radius, 2 * self.radius))
        elif self.type == 'shield':
            scaled_image = pygame.transform.scale(pygame.image.load(shield_path), (2 * self.radius, 2 * self.radius))
        win.blit(scaled_image, (self.x - self.radius, self.y - self.radius))


    def check_collision(self, player):
        # Check if a player has picked up the power-up
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        powerup_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        
        if player_rect.colliderect(powerup_rect):
            return True
        return False
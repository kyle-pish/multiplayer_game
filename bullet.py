import pygame

class Bullet:
    def __init__(self, x, y, vel_x, vel_y, owner):
        self.x = x  # X-coordinate of the bullet's position
        self.y = y  # Y-coordinate of the bullet's position
        self.vel_x = vel_x  # Velocity of the bullet in the x-direction
        self.vel_y = vel_y  # Velocity of the bullet in the y-direction
        self.owner = owner  # Reference to the player who fired the bullet
        self.color = (0, 0, 0)  # Color of the bullet

    def move(self):
        # Move the bullet based on its velocity
        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self, win):
        # Draw the bullet on the game window
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), 5)
        
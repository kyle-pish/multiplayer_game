import pygame

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 0), self.rect)
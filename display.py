import pygame

class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Memory Match Game")

    def clear(self):
        self.screen.fill((0, 0, 0)) 
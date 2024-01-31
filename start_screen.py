import pygame
from config import WIDTH, HEIGHT, FPS
import sys


class Start_screen:
    def __init__(self, surface):
        self.surface = surface
        self.clock = pygame.time.Clock()

        bg = pygame.transform.scale(pygame.image.load('screen.png'), (WIDTH, HEIGHT))
        self.surface.blit(bg, (0, 0))

        # Рендер текста
        font = pygame.font.Font(None, 30)
        text = font.render('Press any key to start the game', 1, (255, 255, 255))
        self.surface.blit(text, (170, 350))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            self.clock.tick(FPS)

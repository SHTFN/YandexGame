import pygame
from config import WIDTH, HEIGHT, FPS
import sys


class Death_screen:
    def __init__(self, surface):
        self.surface = surface

        self.clock = pygame.time.Clock()

        text = ['You died',
                'Press any key to quit']

        bg = pygame.transform.scale(pygame.image.load('data/tiles/start_screen/bg.jpg'), (WIDTH, HEIGHT))
        self.surface.blit(bg, (0, 0))

        # Рендер текста
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.surface.blit(string_rendered, intro_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            self.clock.tick(FPS)
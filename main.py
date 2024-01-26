import pygame
import sys
from config import *
from level import Level
from game_data import level_1


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    level = Level(level_1, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('black')
        level.run()

        pygame.display.update()
        clock.tick(FPS)
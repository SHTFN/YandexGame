import pygame
import sys
from config import *
from level import Level
from game_data import level_1
from start_screen import Start_screen
from death_screen import Death_screen
from statusbar import Statusbar


class Game:
    def __init__(self, surface):
        self.surface = surface

        self.max_health = 100
        self.cur_health = 100
        self.coins = 0

        self.level = Level(level_1, surface, self.change_coin_value, self.coins, self.change_health)



        self.statusbar = Statusbar(self.surface)

    def run_start_screen(self):
        self.start_screen = Start_screen(self.surface)
        self.start_screen.run()

    def change_coin_value(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.cur_health += amount

    def check_game_over(self):
        if self.cur_health <= 0:
            self.cur_health = 100
            self.coins = 0
            self.max_health = 0
            death_screen = Death_screen(self.surface)
            death_screen.run()

    def run(self):
        self.level.run()
        self.statusbar.show_health(self.cur_health, self.max_health)
        self.statusbar.show_coin_value(self.coins)
        self.check_game_over()



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game(screen)

    game.run_start_screen()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game.run()

        pygame.display.update()
        clock.tick(FPS)

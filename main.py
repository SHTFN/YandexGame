import pygame
import sys
from config import *
from level import Level
from game_data import *
from start_screen import Start_screen
from death_screen import Death_screen
from statusbar import Statusbar


class Game:
    def __init__(self, surface, level_num):
        self.surface = surface

        self.max_health = 100  # Максимальное количество здоровья
        self.cur_health = 100  # Количества хдоровья в данный момент
        self.coins = 0  # Количество монет

        if level_num == 1:
            self.level = Level(level_1, surface, self.change_coin_value, self.coins, self.change_health)
        elif level_num == 2:
            self.level = Level(level_2, surface, self.change_coin_value, self.coins, self.change_health)

        self.statusbar = Statusbar(self.surface)  # Создание статусбара

    def run_start_screen(self):  # Запуск стартового экрана
        self.start_screen = Start_screen(self.surface)
        self.start_screen.run()

    def change_coin_value(self, amount):  # Изменение количества собранных монет
        self.coins += amount

    def change_health(self, amount):  # Изменение здоровья игрока
        self.cur_health += amount

    def check_game_over(self):  # Проверка смерти персонажа
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
    level_num = int(input('Введите уровень уровня (на данный момент их 2): '))
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game(screen, level_num)

    game.run_start_screen()  # Стартовый экран

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game.run()  # Запуск уровня

        pygame.display.update()
        clock.tick(FPS)

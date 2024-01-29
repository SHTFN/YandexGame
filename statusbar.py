import pygame


class Statusbar:
    def __init__(self, surface):
        self.surface = surface

        # Создание полосы здоровья
        self.healthbar = pygame.image.load('data/tiles/statusbar/healthbar.png')
        self.healthbar_topleft = (35, 14)
        self.bar_max_width = 70
        self.bar_height = 10

        # Создание счетчика монет
        self.coin_value = pygame.image.load('data/tiles/statusbar/coin.png')
        self.coin_rect = self.coin_value.get_rect(topleft=(12, 30))
        self.font = pygame.font.Font(None, 30)

    def show_health(self, current, full):   # Отображение полосы здоровья
        self.surface.blit(self.healthbar, (10, 10))
        if full != 0:   # Заполнение полосы в зависимости от уровня здоровья
            current_health_ratio = current / full
            current_bar_width = self.bar_max_width * current_health_ratio
            healthbar_rect = pygame.Rect(self.healthbar_topleft, (current_bar_width, self.bar_height))
            pygame.draw.rect(self.surface, '#dc4949', healthbar_rect)

    def show_coin_value(self, amount):  # Отображение счетчика монет
        self.surface.blit(self.coin_value, self.coin_rect)
        coin_amount_surf = self.font.render(str(amount), False, '#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery))
        self.surface.blit(coin_amount_surf, coin_amount_rect)

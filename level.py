import pygame
from help_functions import import_csv_layout
from config import tile_size, WIDTH, HEIGHT
from tiles import Tile, StaticTile, Crate, Coin, Enemy, Water
from player import Player
from result_screen import Result_screen


class Level:
    def __init__(self, level_data, surface, change_coins, cur_coins, change_health):
        self.surface = surface
        self.world_shift = 0

        # Создание стартовой и финальной точек игрока
        player_layer = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layer, change_health)

        self.change_coins = change_coins    # Функция увеличения количества монет
        self.cur_coins = cur_coins

        self.win = False

        # Создание групп слоёв спрайтов
        # Земля
        terrain_layer = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layer, 'terrain')
        # Трава
        grass_layer = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layer, 'grass')
        # Ящики и прочие предметы
        crate_layer = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layer, 'crates')
        # Монеты
        coins_layer = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layer, 'coins')
        # Деревья
        trees_layer = import_csv_layout(level_data['trees'])
        self.trees_sprites = self.create_tile_group(trees_layer, 'trees')
        # Ограничители движения врагов
        constraints_layer = import_csv_layout(level_data['constraints'])
        self.constraints_sprites = self.create_tile_group(constraints_layer, 'constraints')
        # Враги
        enemies_layer = import_csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(enemies_layer, 'enemies')
        # Длина уровня для отрисовки воды
        level_width = len(terrain_layer[0]) * tile_size
        self.water = Water(HEIGHT - 40, level_width)

    # Добавление спрайтов в соответствующие группы
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell != '-1':    # Если клетка не пустая
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        if int(cell) < 10:
                            sprite = StaticTile(tile_size, x, y,
                                                pygame.image.load(f'data/tiles/terrain/tile_000{cell}.png'))
                        elif int(cell) < 100:
                            sprite = StaticTile(tile_size, x, y,
                                                pygame.image.load(f'data/tiles/terrain/tile_00{cell}.png'))
                        elif int(cell) < 1000:
                            sprite = StaticTile(tile_size, x, y,
                                                pygame.image.load(f'data/tiles/terrain/tile_0{cell}.png'))
                    elif type == 'grass':
                        sprite = StaticTile(tile_size, x, y, pygame.image.load(f'data/tiles/grass/tile_0{cell}.png'))
                    elif type == 'trees':
                        if int(cell) < 100:
                            sprite = StaticTile(tile_size, x, y,
                                                pygame.image.load(f'data/tiles/trees/tile_00{cell}.png'))
                        else:
                            sprite = StaticTile(tile_size, x, y,
                                                pygame.image.load(f'data/tiles/trees/tile_0{cell}.png'))
                    elif type == 'crates':
                        sprite = Crate(tile_size, x, y)
                    elif type == 'coins':
                        sprite = Coin(tile_size, x, y, 'data/tiles/coins')
                    elif type == 'enemies':
                        sprite = Enemy(tile_size, x, y)
                    elif type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    # Добавление стартовой и конечной точек игрока
    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == '111':
                    sprite = Player((x, y), change_health)
                    self.player.add(sprite)
                elif cell == '67':
                    hat_surface = pygame.image.load('data/tiles/diamond/tile.png')
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    # Коллизия врагов
    def enemy_collision(self):
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints_sprites, False):
                enemy.reverse()

    # Горизонтальная коллизия игрока
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        objects = self.terrain_sprites.sprites() + self.crate_sprites.sprites()

        for sprite in objects:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    # Вертикальная коллизия игрока
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        objects = self.terrain_sprites.sprites() + self.crate_sprites.sprites()

        for sprite in objects:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    # Движение камеры
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < WIDTH / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > WIDTH - (WIDTH / 4) and direction_x > 0:

            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    # Проверка смерти игрока
    def check_death(self):
        if self.player.sprite.rect.y > HEIGHT:
            text = ['You died',
                    'Press any key to restart']
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

    # Проверка победы игрока
    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.win = True
            if True:
                text = ['You won!',
                        f'You collected {self.cur_coins} coins']
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
            #   sleep(5)
            result_screen = Result_screen(self.surface, self.cur_coins)
            result_screen.run()

    # Коллизия монет с игроком
    def check_coin_collisions(self):
        coins = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)
        if coins:
            for _ in coins:
                self.cur_coins += 1
                self.change_coins(1)

    # Коллизия врагов с игроком
    def check_enemy_collision(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemies_sprites, False)
        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                # Проверка того, атакует ли игрок врагов путём прыжка на них, или же получает от них урон
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -7
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    # Отрисовка всех спрайтов
    def run(self):
        bg = pygame.transform.scale(pygame.image.load('data/tiles/sky.png'), (WIDTH, HEIGHT))
        self.surface.blit(bg, (0, 0))

        self.terrain_sprites.draw(self.surface)
        self.terrain_sprites.update(self.world_shift)

        self.grass_sprites.draw(self.surface)
        self.grass_sprites.update(self.world_shift)

        self.trees_sprites.draw(self.surface)
        self.trees_sprites.update(self.world_shift)

        self.enemies_sprites.draw(self.surface)
        self.constraints_sprites.update(self.world_shift)
        self.enemy_collision()
        self.enemies_sprites.update(self.world_shift)

        self.crate_sprites.draw(self.surface)
        self.crate_sprites.update(self.world_shift)

        self.coins_sprites.draw(self.surface)
        self.coins_sprites.update(self.world_shift)

        self.player.draw(self.surface)
        self.player.update()
        # self.check_damage()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.goal.draw(self.surface)
        self.goal.update(self.world_shift)

        self.check_death()
        self.check_win()

        self.check_coin_collisions()
        self.check_enemy_collision()

        self.water.draw(self.surface)

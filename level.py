import pygame
import sys
from tiles import Tile
from player import Player
from config import tile_size, WIDTH, HEIGHT


class Level:
    def __init__(self, level_data, surface):
        self.pause = False
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for y, row in enumerate(layout):
            for x, cell in enumerate(row):
                if cell == 'X':
                    tile = Tile((x * tile_size, y * tile_size), tile_size)
                    self.tiles.add(tile)
                if cell == '@':
                    player_sprite = Player((x * tile_size, y * tile_size))
                    self.player.add(player_sprite)

    def scrool_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < WIDTH / 5 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > WIDTH - (WIDTH / 5) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_collision(self):
        player = self.player.sprite

        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    def vertical_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    def check_player_death_by_height(self):
        player = self.player.sprite
        if player.rect.y > HEIGHT:
            self.running = False

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        self.player.update()
        self.horizontal_collision()
        self.vertical_collision()
        self.check_player_death_by_height()
        self.player.draw(self.display_surface)

        self.scrool_x()
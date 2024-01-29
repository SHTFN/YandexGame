import pygame
from help_functions import import_folder
from random import randint
from config import WIDTH


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        #self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x_shift):
        self.rect.x += x_shift


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class Crate(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('data/tiles/crates/tile_0026.png'))
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift


class Coin(AnimatedTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))


class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'data/tiles/enemies/run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(2, 4)

    def move(self):
        self.rect.x += self.speed

    def flip_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()
        self.move()
        self.flip_image()


class Water:
    def __init__(self, top, level_width):
        water_start = -WIDTH
        water_tile_width = 18
        tile_x_amount = int((level_width + WIDTH) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            #print(x)
            y = top + water_tile_width
            #print(y)

            sprite = AnimatedTile(18, x, y, 'data/tiles/water')
            #print(sprite)
            self.water_sprites.add(sprite)
        #print(len(self.))

    def draw(self, surface):
        self.water_sprites.update(0)
        self.water_sprites.draw(surface)


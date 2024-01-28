import pygame
from help_functions import import_csv_layout, import_cut_graphics
from config import tile_size
from tiles import Tile, StaticTile


class Level:
    def __init__(self, level_data, surface):
        self.surface = surface
        self.world_shift = 0

        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('data/tiles/terrain_tilemap.png')
                        tile_surface = terrain_tile_list[int(cell)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

        return sprite_group

    def run(self):
        self.terrain_sprites.draw(self.surface)
        self.terrain_sprites.update(self.world_shift)

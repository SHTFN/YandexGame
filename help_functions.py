from os import walk
import pygame.image


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        # kpath = path
        for image in img_files:
            full_path = path + '/' + image
            print(full_path)
            try:
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
            except Exception:
                pass

    return surface_list


import_folder('data/sprites/Player sprites')
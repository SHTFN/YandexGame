import pygame
from help_functions import import_folder
from time import sleep


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        self.status = 'idle'
        self.facing_to_right = True
        self.attack = False
        self.on_ground = True

    def import_character_assets(self):
        character_path = 'data/sprites/Player sprites/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'attack': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_to_right:
            self.image = image
        else:
            flip_image = pygame.transform.flip(image, True, False)
            self.image = flip_image

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.rect.y -= 1
            self.facing_to_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.rect.y -= 1
            self.facing_to_right = True
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.direction.y == 0.0:
            self.jump()

        if keys[pygame.K_f]:
            self.attack = True

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
            self.on_ground = False
        elif self.direction.y > 1:
            self.status = 'fall'
            self.on_ground = False
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

        if self.attack:
            self.status = 'attack'
            #sleep(self.animation_speed)
            self.attack = False

    def update(self):
        self.get_input()
        #self.rect.x += self.direction.x * self.speed
        #self.apply_gravity()
        self.get_status()
        self.animate()
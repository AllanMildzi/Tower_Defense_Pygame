import pygame, os
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, enemy_type, pos):
        super().__init__(group)
        self.screen = pygame.display.get_surface()
        self.enemy_type = enemy_type
        self.direction = "right"

        # Loads the assets
        for index, info in enumerate(os.walk(f"../graphics/enemy/{enemy_type}")):
            if index == 0:
                self.assets = {direction: [] for direction in info[1]}
            else:
                for sprite in info[2]:
                    direction = list(self.assets.keys())[index-1]
                    full_path = f"../graphics/enemy/{enemy_type}/{direction}/{sprite}"
                    surf = pygame.image.load(full_path).convert_alpha()
                    surf = pygame.transform.rotozoom(surf, 0, 1.2)
                    self.assets[direction].append(surf)

        self.index = 0
        self.image = self.assets[self.direction][self.index]
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.path = [pygame.math.Vector2(self.pos), 
                    pygame.math.Vector2(self.pos.x + 500, self.pos.y),
                    pygame.math.Vector2(self.pos.x + 500, self.pos.y + 200)]
        self.path_index = 0

        self.speed = 1

    def animation_state(self):
        self.index += 0.1
        if self.index >= len(self.assets[self.direction]):
            self.index = 0

        self.image = self.assets[self.direction][int(self.index)]

    def define_path(self):
        current_path = self.path[self.path_index]

        if self.pos == self.path[self.path_index+1]:
            if self.pos == self.path[len(self.path)-1]:
                return False
            
            self.path_index += 1
            current_path = self.path[self.path_index]
        
        if self.path[self.path_index+1].x == current_path.x:
            self.pos.y += self.speed
        elif self.path[self.path_index+1].y == current_path.y:
            self.pos.x += self.speed

        return True

    def update(self):
        self.animation_state()
        if not self.define_path():
            self.kill()
        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y)
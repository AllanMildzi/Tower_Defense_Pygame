import pygame, os, random
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, enemy_type, pos):
        super().__init__(group)
        self.screen = pygame.display.get_surface()
        self.enemy_type = enemy_type
        self.state = "walk"

        # Loads the assets
        for index, info in enumerate(os.walk(f"../graphics/enemy/{enemy_type}")):
            if index == 0:
                self.assets = {state: [] for state in info[1]}
            else:
                for sprite in info[2]:
                    state = list(self.assets.keys())[index-1]
                    full_path = f"../graphics/enemy/{enemy_type}/{state}/{sprite}"
                    surf = pygame.image.load(full_path).convert_alpha()
                    surf = pygame.transform.rotozoom(surf, 0, 0.35)
                    self.assets[state].append(surf)

        self.index = 0
        self.image = self.assets[self.state][self.index]
        self.rect = self.image.get_rect(topleft = pos)
        
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(1, 1)
        self.speed = 1

        self.health = 100

        self.top_path = [pygame.math.Vector2(self.pos),
                        pygame.math.Vector2(4 * TILE_WIDTH, self.pos.y),
                        pygame.math.Vector2(4 * TILE_WIDTH, self.pos.y - (2 * TILE_HEIGHT)),
                        pygame.math.Vector2(6 * TILE_WIDTH, self.pos.y - (2 * TILE_HEIGHT)),
                        pygame.math.Vector2(6 * TILE_WIDTH, self.pos.y - (3 * TILE_HEIGHT)),
                        pygame.math.Vector2(10 * TILE_WIDTH, self.pos.y - (3 * TILE_HEIGHT)),
                        pygame.math.Vector2(10 * TILE_WIDTH, self.pos.y - TILE_HEIGHT),
                        pygame.math.Vector2(13 * TILE_WIDTH, self.pos.y - TILE_HEIGHT),
                        pygame.math.Vector2(13 * TILE_WIDTH, self.pos.y - (2 * TILE_HEIGHT)),
                        pygame.math.Vector2(15 * TILE_WIDTH, self.pos.y - (2 * TILE_HEIGHT))]

        self.bottom_path = [pygame.math.Vector2(self.pos),
                            pygame.math.Vector2(2 * TILE_WIDTH, self.pos.y),
                            pygame.math.Vector2(2 * TILE_WIDTH, self.pos.y + (3 * TILE_HEIGHT)),
                            pygame.math.Vector2(6 * TILE_WIDTH, self.pos.y + (3 * TILE_HEIGHT)),
                            pygame.math.Vector2(6 * TILE_WIDTH, self.pos.y + (2 * TILE_HEIGHT)),
                            pygame.math.Vector2(9 * TILE_WIDTH, self.pos.y + (2 * TILE_HEIGHT)),
                            pygame.math.Vector2(9 * TILE_WIDTH, self.pos.y + (4 * TILE_HEIGHT)),
                            pygame.math.Vector2(12 * TILE_WIDTH, self.pos.y + (4 * TILE_HEIGHT)),
                            pygame.math.Vector2(12 * TILE_WIDTH, self.pos.y + (3 * TILE_HEIGHT)),
                            pygame.math.Vector2(14 * TILE_WIDTH, self.pos.y + (3 * TILE_HEIGHT)),
                            pygame.math.Vector2(14 * TILE_WIDTH, self.pos.y + (2 * TILE_HEIGHT)),
                            pygame.math.Vector2(15 * TILE_WIDTH, self.pos.y + (2 * TILE_HEIGHT))]

        self.path = random.choice((self.top_path, self.bottom_path))        
        self.path_index = 0

    def animation_state(self):
        self.image = self.assets[self.state][int(self.index)]
        self.index += 0.2
        if self.index >= len(self.assets[self.state]):
            if self.state != "die":
                self.index = 0
            else:
                self.kill()

    def draw_health_bar(self):
        pygame.draw.rect(self.screen, GREEN, (self.rect.left, self.rect.top, self.rect.width / 2, 10))

    def get_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.state = "die"
            self.index = 0
            self.speed = 0

    def update_path(self):
        current_path = self.path[self.path_index]

        if self.pos == self.path[self.path_index+1]:
            if self.pos == self.path[len(self.path)-1]:
                return False
            
            self.path_index += 1
            current_path = self.path[self.path_index]

            if current_path.y > abs(self.path[self.path_index+1].y):
                self.direction.y = -1
            else:
                self.direction.y = 1
        
        if self.path[self.path_index+1].x == current_path.x:
            self.pos.y += self.speed * self.direction.y
        elif self.path[self.path_index+1].y == current_path.y:
            self.pos.x += self.speed * self.direction.x

        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y)

        return True

    def update(self):
        self.animation_state()
        self.draw_health_bar()
        if not self.update_path():
            print("enemy killed")
            self.kill()
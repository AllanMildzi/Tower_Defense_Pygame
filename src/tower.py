import pygame
from settings import *
from circle import Circle
from projectile import Projectile

class Tower(pygame.sprite.Sprite):
    def __init__(self, group, pos, tower_type, surfacemaker):
        super().__init__(group)
        self.screen = pygame.display.get_surface()
        self.pos = pygame.math.Vector2(pos)
        self.tower_type = tower_type
        self.surfacemaker = surfacemaker

        self.top_y = 50
        self.image = self.surfacemaker.get_surf(self.tower_type, (TOWER_RECT_WIDTH, TOWER_RECT_HEIGHT), self.top_y)
        self.rect = self.image.get_rect(center = self.pos)
        self.circle = Circle(self.pos, TILE_WIDTH * 2)

        self.is_placed = False
        self.is_shooting = False
        self.projectile_sprites = pygame.sprite.Group()
        self.projectile_sprites.add(Projectile(self.projectile_sprites, "_".join(self.tower_type.split("_")[:2]), (self.pos.x, self.pos.y - 10)))

        if tower_type == "stone_tower_1":
            self.damage = 10
        elif tower_type == "rock_tower_1":
            self.damage = 50

    def move_tower(self, pos):
        self.rect.center = pos
        self.circle.rect.center = pos
        for projectile_sprite in self.projectile_sprites:
            projectile_sprite.rect.center = pos

    def shooting_animation(self):
        self.top_y -= 1
        for projectile in self.projectile_sprites:
            if self.top_y < 0:
                projectile.rect.y += 1
            else:
                projectile.rect.y -= 1
            if self.top_y == 0:
                projectile.can_move = True
        
        if abs(self.top_y) >= 50:
            self.top_y = 50
            self.is_shooting = False
            if self.is_placed:
                self.projectile_sprites.add(Projectile(self.projectile_sprites, "_".join(self.tower_type.split("_")[:2]), (self.pos.x, self.pos.y - 10)))
        self.image = self.surfacemaker.get_surf(self.tower_type, (TOWER_RECT_WIDTH, TOWER_RECT_HEIGHT), abs(self.top_y))

    def upgrade(self, money):
        if self.tower_type == "stone_tower_1":
            self.tower_type = "stone_tower_2"
            self.circle.radius = TILE_WIDTH * 2.25
            self.damage = 20
        elif self.tower_type == "stone_tower_2":
            self.tower_type = "stone_tower_3"
            self.circle.radius = TILE_WIDTH * 2.5
            self.damage = 40

        elif self.tower_type == "rock_tower_1":
            self.tower_type = "rock_tower_2"
            self.circle.radius = TILE_WIDTH * 2.25
            self.damage = 20
        elif self.tower_type == "rock_tower_2":
            self.tower_type = "rock_tower_3"
            self.circle.radius = TILE_WIDTH * 2.5
            self.damage = 40
        self.image = self.surfacemaker.get_surf(self.tower_type, (TOWER_RECT_WIDTH, TOWER_RECT_HEIGHT), self.top_y)

    def update(self, pos):
        self.circle.draw(self.screen)
        if not self.is_placed:
            self.move_tower(pos)
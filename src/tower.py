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

        self.top_y = 60
        self.image = self.surfacemaker.get_surf(self.tower_type, (TILE_WIDTH * 3 / 2, TILE_HEIGHT * 2), self.top_y)
        self.rect = self.image.get_rect(center = self.pos)
        self.circle = Circle(self.pos, TILE_WIDTH * 2)

        self.is_shooting = False
        self.projectile_sprites = pygame.sprite.Group()
        self.projectile_sprites.add(Projectile(self.projectile_sprites, (self.pos.x, self.pos.y - 10)))

    def shooting_animation(self):
        self.top_y -= 1
        for projectile in self.projectile_sprites:
            if self.top_y < 0:
                projectile.rect.y += 1
            else:
                projectile.rect.y -= 1
        
        if abs(self.top_y) >= 60:
            self.top_y = 60
            self.is_shooting = False
            self.projectile_sprites.add(Projectile(self.projectile_sprites, (self.pos.x, self.pos.y - 10)))
        self.image = self.surfacemaker.get_surf(self.tower_type, (TILE_WIDTH * 3 / 2, TILE_HEIGHT * 2), abs(self.top_y))

    def update(self):
        self.circle.draw(self.screen)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
import pygame, math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)

        self.image = pygame.image.load("../graphics/projectile/stone.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)

        self.start = pygame.math.Vector2(pos)
        self.end = pygame.math.Vector2()

        self.speed = 5

    def move(self):
        angle = math.atan2((self.end.y - self.rect.y), (self.end.x - self.rect.x))
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)
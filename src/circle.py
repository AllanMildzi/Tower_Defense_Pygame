import pygame
from settings import *

class Circle(pygame.sprite.Sprite):
    def __init__(self, pos, radius):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((MAX_RADIUS, MAX_RADIUS))
        self.image.set_colorkey((0, 0, 0))
        self.image.fill((0, 0, 0))
        self.image.set_alpha(90)
        
        self.radius = radius
        self.pos = pos
        
        pygame.draw.circle(self.image, (0, 0, 255), (MAX_RADIUS / 2, MAX_RADIUS / 2), self.radius)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = self.pos)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
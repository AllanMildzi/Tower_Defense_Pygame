import pygame
from settings import *

class Circle(pygame.sprite.Sprite):
    def __init__(self, pos, radius):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((MAX_RADIUS, MAX_RADIUS))
        self.image.set_colorkey(BLACK)
        self.image.fill(BLACK)
        self.image.set_alpha(CIRCLE_ALPHA)
        
        self.radius = radius
        self.color = CIRCLE_RED        
        self.rect = self.image.get_rect(center=pos)
    
    def draw(self, surface):
        pygame.draw.circle(self.image, self.color, (MAX_RADIUS / 2, MAX_RADIUS / 2), self.radius)
        surface.blit(self.image, self.rect)
import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, group, tile_type, pos):
        super().__init__(group)
        self.tile_type = tile_type
        self.pos = pos

        self.image = pygame.image.load(f"../graphics/tiles/{TILE_LEGEND[self.tile_type]}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect(topleft = pos)
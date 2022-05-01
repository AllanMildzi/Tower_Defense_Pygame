import pygame, os
from settings import *

class SurfaceMaker():
    def __init__(self):
        for index, info in enumerate(os.walk("../graphics/tower")):
            if index == 0:
                self.assets = {tower_type:{} for tower_type in info[1]}
            else:
                for image_name in info[2]:
                    tower_type = list(self.assets.keys())[index - 1]
                    full_path = f"../graphics/tower/{tower_type}/{image_name}"
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.assets[tower_type][image_name.split(".")[0]] = surf

    def get_surf(self, tower_type, size, current_y):
        image = pygame.Surface(size)
        image.set_colorkey(BLACK)

        sides = self.assets[tower_type]

        scaled_bottom = pygame.transform.scale(sides["bottom"], (size[0], size[1]))
        scaled_top_1 = pygame.transform.scale(sides["top_1"], (size[0], sides["top_1"].get_height() * 0.75))
        scaled_top_2 = pygame.transform.scale(sides["top_2"], (size[0], sides["top_2"].get_height() * 0.75))
        
        image.blit(scaled_top_2, (0, current_y))
        image.blit(scaled_bottom, (0, 0))
        image.blit(scaled_top_1, (0, scaled_top_2.get_height() - 2 + current_y))

        return image
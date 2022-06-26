import pygame, math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, group, tower_type, pos):
        super().__init__(group)

        if tower_type == "stone_tower":
            self.image = pygame.image.load("../graphics/projectile/stone.png").convert_alpha()
        elif tower_type == "rock_tower":
            self.image = pygame.image.load("../graphics/projectile/rock.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 0.75, self.image.get_height() * 0.75))
        
        self.rect = self.image.get_rect(center=pos)

        self.target = None
        self.can_move = False
        self.speed = 10

    def move(self):
        angle = math.atan2((self.target.rect.center[1] - self.rect.center[1]), (self.target.rect.center[0] - self.rect.center[0]))
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)
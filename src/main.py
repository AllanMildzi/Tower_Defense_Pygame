import pygame, sys
from settings import *
from tile import Tile
from enemy import Enemy
from tower import Tower
from surfacemaker import SurfaceMaker

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.tile_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.tower_sprites = pygame.sprite.Group()

        self.surfacemaker = SurfaceMaker()
        Enemy(self.enemy_sprites, "red_goblin", (-TILE_WIDTH, (4 * TILE_HEIGHT) - TILE_HEIGHT // 3))
        Enemy(self.enemy_sprites, "green_goblin", (-TILE_WIDTH * 2, (4 * TILE_HEIGHT) - TILE_HEIGHT // 3))
        Tower(self.tower_sprites, (120, 200), "stone_tower_1", self.surfacemaker)
        Tower(self.tower_sprites, (400, 200), "stone_tower_2", self.surfacemaker)

        self.setup_map()

    def setup_map(self):
        for row_index, row in enumerate(TILE_MAP):
            y = row_index * TILE_HEIGHT
            for col_index, col in enumerate(row):
                x = col_index * TILE_WIDTH
                Tile(self.tile_sprites, col, (x, y))

    def enemy_tower_collision(self):
        for sprite in self.tower_sprites:
            overlap_sprites = pygame.sprite.spritecollide(sprite.circle, self.enemy_sprites, False, pygame.sprite.collide_mask)
            for enemy_sprite in overlap_sprites:
                if enemy_sprite.state == "die":
                    overlap_sprites.remove(enemy_sprite)
            
            if overlap_sprites:
                sprite.is_shooting = True
                for projectile in sprite.projectile_sprites:
                    projectile.end = overlap_sprites[0].pos
            if sprite.is_shooting:
                sprite.shooting_animation()

    def projectile_enemy_collision(self):
        for tower in self.tower_sprites:
            for projectile in tower.projectile_sprites:
                overlap_sprites = pygame.sprite.spritecollide(projectile, self.enemy_sprites, False)
                if overlap_sprites:
                    overlap_sprites[0].get_damage(20)
                    projectile.kill()
                elif tower.top_y <= 0:
                    projectile.move()

    def run(self):
        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.tile_sprites.draw(self.screen)
            self.tower_sprites.draw(self.screen)
            for tower in self.tower_sprites:
                tower.projectile_sprites.draw(self.screen)
            self.enemy_sprites.draw(self.screen)
            
            self.enemy_sprites.update()
            self.tower_sprites.update()
            self.enemy_tower_collision()
            self.projectile_enemy_collision()
            
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
import pygame, sys
from settings import *
from tile import Tile
from enemy import Enemy
from tower import Tower
from surfacemaker import SurfaceMaker
from ui import UI

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.tile_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.tower_sprites = pygame.sprite.Group()

        self.surfacemaker = SurfaceMaker()
        self.ui = UI()
        Enemy(self.enemy_sprites, "red_goblin", (-TILE_WIDTH, (4 * TILE_HEIGHT) - TILE_HEIGHT // 3))
        Enemy(self.enemy_sprites, "green_goblin", (-TILE_WIDTH * 2, (4 * TILE_HEIGHT) - TILE_HEIGHT // 3))

        self.setup_map()

    def setup_map(self):
        for row_index, row in enumerate(TILE_MAP):
            y = row_index * TILE_HEIGHT
            for col_index, col in enumerate(row):
                x = col_index * TILE_WIDTH
                Tile(self.tile_sprites, col, (x, y))

    def enemy_tower_collision(self):
        for tower in self.tower_sprites:
            overlap_sprites = pygame.sprite.spritecollide(tower.circle, self.enemy_sprites, False, pygame.sprite.collide_mask)
            for enemy_sprite in overlap_sprites:
                if enemy_sprite.state == "die":
                    overlap_sprites.remove(enemy_sprite)
            
            if overlap_sprites and tower.is_placed:
                overlap_sprites[0].is_target = True
                tower.is_shooting = True
                for projectile in tower.projectile_sprites:
                    if not projectile.can_move:
                        projectile.end = overlap_sprites[0].pos
            if tower.is_shooting:
                tower.shooting_animation()

    def projectile_enemy_collision(self):
        for tower in self.tower_sprites:
            for projectile in tower.projectile_sprites:
                overlap_sprites = pygame.sprite.spritecollide(projectile, self.enemy_sprites, False)
                for enemy in overlap_sprites:
                    if not enemy.is_target:
                        overlap_sprites.remove(enemy)
                
                if tower.is_placed and overlap_sprites:
                    for enemy in overlap_sprites:
                        enemy.get_damage(tower.damage)
                        enemy.is_target = False
                        projectile.kill()
                elif projectile.can_move:
                    projectile.move()

    def check_tower_availibility(self):
        for tower in self.tower_sprites:
            overlap_sprites = pygame.sprite.spritecollide(tower, self.tile_sprites, False)
            for tile_sprite in overlap_sprites:
                if tile_sprite.tile_type == "1" or tower.rect.colliderect(self.ui.ui_rect):
                    tower.circle.color = CIRCLE_RED
                    break
                else:
                    tower.circle.color = CIRCLE_BLUE

    def user_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for box in self.ui.tower_box_list:
                        if box.rect.collidepoint(event.pos):
                            if box.box_type == "stone":
                                Tower(self.tower_sprites, event.pos, "stone_tower_1", self.surfacemaker)
                            elif box.box_type == "rock":
                                Tower(self.tower_sprites, event.pos, "rock_tower_1", self.surfacemaker)
                    
                    for tower in self.tower_sprites:
                        if not tower.is_placed and tower.circle.color != CIRCLE_RED:
                            tower.is_placed = True
                            tower.pos = tower.circle.pos = pygame.math.Vector2(event.pos)
                            tower.circle.image.set_alpha(0)
                        elif tower.is_placed and tower.rect.collidepoint(event.pos):
                            for prev_tower in self.tower_sprites:
                                if prev_tower == tower:
                                    continue
                                prev_tower.circle.image.set_alpha(0)
                            if tower.circle.image.get_alpha() == 0:
                                tower.circle.image.set_alpha(CIRCLE_ALPHA)
                                if tower.tower_type.split("_")[2] != "3" and self.ui.money >= UPGRADE_PRICES[tower.tower_type]:
                                    self.ui.can_draw_upgrade = True
                            else:
                                tower.circle.image.set_alpha(0)
                                self.ui.can_draw_upgrade = False
                        elif tower.circle.image.get_alpha() == CIRCLE_ALPHA and self.ui.can_draw_upgrade and self.ui.upgrade_box.rect.collidepoint(event.pos):
                            tower.upgrade(self.ui.money)

                else:
                    for tower_sprite in self.tower_sprites:
                        if not tower_sprite.is_placed:
                            tower_sprite.kill()

    def run(self):
        while True:
            self.clock.tick(FPS)

            self.screen.fill(GREEN)
            self.tile_sprites.draw(self.screen)
            self.enemy_sprites.draw(self.screen)
            self.tower_sprites.draw(self.screen)
            self.ui.display()
            for tower in self.tower_sprites:
                tower.projectile_sprites.draw(self.screen)
            
            self.user_events()
            self.enemy_sprites.update(self.ui)
            self.tower_sprites.update(pygame.mouse.get_pos())
            
            self.enemy_tower_collision()
            self.projectile_enemy_collision()
            self.check_tower_availibility()
            
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
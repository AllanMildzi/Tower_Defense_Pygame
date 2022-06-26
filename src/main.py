import pygame, sys, random, math

from settings import *
from tile import Tile
from enemy import Enemy
from tower import Tower
from surfacemaker import SurfaceMaker
from ui import UI

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.tile_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.tower_sprites = pygame.sprite.Group()

        self.surfacemaker = SurfaceMaker()
        self.ui = UI()

        self.enemies_per_wave = 10
        self.curr_enemy_count = 0

        self.enemy_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer, 2000)

        self.setup_map()

    def setup_map(self):
        for row_index, row in enumerate(TILE_MAP):
            y = row_index * TILE_HEIGHT
            for col_index, col in enumerate(row):
                x = col_index * TILE_WIDTH
                Tile(self.tile_sprites, col, (x, y))

    def distance(self, start, end):
        return math.sqrt(((end.x - start.x) ** 2) + ((end.y - start.y) ** 2))

    def enemy_tower_collision(self):
        for tower in self.tower_sprites:
            overlap_sprites = []
            for enemy_sprite in self.enemy_sprites:
                if enemy_sprite.state != "die" and self.distance(tower.pos, pygame.math.Vector2(enemy_sprite.rect.center)) <= tower.circle.radius:
                    overlap_sprites.append(enemy_sprite)

            overlap_sprites.sort(key=lambda enemy: enemy.pos.x)
            overlap_sprites = overlap_sprites[::-1]
            
            if overlap_sprites and tower.is_placed and not tower.is_shooting:
                tower.is_shooting = True
                for projectile in tower.projectile_sprites:
                    projectile.target = overlap_sprites[0]

    def projectile_enemy_collision(self):
        for tower in self.tower_sprites:
            for projectile in tower.projectile_sprites:
                if projectile.can_move and projectile.target != None:
                    projectile.move()
                    if self.distance(pygame.math.Vector2(projectile.rect.center), pygame.math.Vector2(projectile.target.rect.center)) <= 5:
                        projectile.target.get_damage(tower.damage)
                        projectile.target = None
                        projectile.kill()

    def check_tower_availibility(self):
        moving_tower = None
        placed_towers = []
        sand_tiles = [tile for tile in self.tile_sprites if tile.tile_type == "1"]
        for tower in self.tower_sprites:
            if tower.is_placed:
                placed_towers.append(tower)
            else:
                moving_tower = tower
        
        if moving_tower != None:            
            if (pygame.sprite.spritecollide(moving_tower, placed_towers, False)
                or pygame.sprite.spritecollide(moving_tower, sand_tiles, False)
                or moving_tower.rect.colliderect(self.ui.ui_rect)):
                
                moving_tower.circle.color = CIRCLE_RED
            else:
                moving_tower.circle.color = CIRCLE_BLUE

    def reset_circle_alpha(self):
        for tower in self.tower_sprites:
            tower.circle.image.set_alpha(0)
            tower.can_upgrade = False
            
    def spawn_enemy(self):
        if self.curr_enemy_count < self.enemies_per_wave:
            if self.ui.wave <= 5:
                enemy_list = ENEMY_TYPES[:2]
            elif self.ui.wave <= 10:
                enemy_list = ENEMY_TYPES[:3]
            else:
                enemy_list = ENEMY_TYPES
            
            Enemy(self.enemy_sprites, random.choice(enemy_list), (random.randint(-200, -100), (4 * TILE_HEIGHT) - TILE_HEIGHT // 3))
            self.curr_enemy_count += 1
        if len(self.enemy_sprites) <= 0:
            self.ui.wave += 1
            self.enemies_per_wave += 10
            self.curr_enemy_count = 0

    def user_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.enemy_timer:
                self.spawn_enemy()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for box in self.ui.tower_box_list:
                        if box.rect.collidepoint(event.pos):
                            self.reset_circle_alpha()
                            if box.box_type == "stone" and self.ui.money >= 500:
                                Tower(self.tower_sprites, event.pos, "stone_tower_1", self.surfacemaker)
                            elif box.box_type == "rock" and self.ui.money >= 1000:
                                Tower(self.tower_sprites, event.pos, "rock_tower_1", self.surfacemaker)
                    
                    for tower in self.tower_sprites:
                        if not tower.is_placed and tower.circle.color != CIRCLE_RED:
                            tower.is_placed = True
                            tower.pos = tower.circle.pos = pygame.math.Vector2(event.pos)
                            tower.circle.image.set_alpha(0)
                            self.ui.money -= TOWER_PRICES[tower.tower_type]
                        
                        elif tower.is_placed and tower.rect.collidepoint(event.pos):
                            self.reset_circle_alpha()
                            if tower.circle.image.get_alpha() == 0:
                                tower.circle.image.set_alpha(CIRCLE_ALPHA)
                                if tower.tower_type.split("_")[2] != "3" and self.ui.money >= UPGRADE_PRICES[tower.tower_type]:
                                    tower.can_upgrade = True
                            else:
                                tower.circle.image.set_alpha(0)
                                tower.can_upgrade = False
                        
                        elif tower.circle.image.get_alpha() == CIRCLE_ALPHA and tower.can_upgrade and self.ui.upgrade_box.rect.collidepoint(event.pos):
                            tower.upgrade(self.ui)
                            tower.circle.image.set_alpha(0)
                            tower.can_upgrade = False
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
                if tower.is_shooting:
                    tower.shooting_animation()
                if tower.can_upgrade:
                    self.ui.draw_upgrade_box(UPGRADE_PRICES[tower.tower_type])
            
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
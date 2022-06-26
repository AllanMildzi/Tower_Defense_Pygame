import pygame
from settings import *

class UI:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.ui_rect = pygame.Rect(WIDTH - UI_WIDTH, 0, UI_WIDTH, HEIGHT)
        self.text_font = pygame.font.Font("../font/ARCADEPI.TTF", 20)

        self.health = 100
        self.money = 10000
        self.wave = 1

        self.health_surf = pygame.image.load("../graphics/ui/heart.png").convert_alpha()
        self.health_surf = pygame.transform.rotozoom(self.health_surf, 0, 0.1)
        self.health_surf_rect = self.health_surf.get_rect(topleft=(GAME_WIDTH + 20, 70))
        self.health_text = self.text_font.render(f"{str(self.health)}/100", False, BLACK)
        self.health_text_rect = self.health_text.get_rect(center=(self.health_surf_rect.center[0] + 90,
                                                                  self.health_surf_rect.center[1]))

        self.coin_surf = pygame.image.load("../graphics/ui/coin.png").convert_alpha()
        self.coin_surf = pygame.transform.rotozoom(self.coin_surf, 0, 0.1)
        self.coin_surf_rect = self.coin_surf.get_rect(topleft=(GAME_WIDTH + 20, 120))
        self.money_text = self.text_font.render(str(self.money), False, BLACK)
        self.money_text_rect = self.money_text.get_rect(center=(self.coin_surf_rect.center[0] + 75,
                                                                self.coin_surf_rect.center[1]))

        self.wave_text = self.text_font.render(f"Wave: {str(self.wave)}", False, BLACK)
        self.wave_text_rect = self.wave_text.get_rect(center=(GAME_WIDTH + (UI_WIDTH / 2), 30))

        self.tower_box_list = [Box("stone", (GAME_WIDTH + (UI_WIDTH / 2), 300)),
                               Box("rock", (GAME_WIDTH + (UI_WIDTH / 2), 450))]
        self.upgrade_box = Box("upgrade", (GAME_WIDTH + (UI_WIDTH / 2), HEIGHT - 70))

    def draw_tower_boxes(self):
        pygame.draw.line(self.screen, BLACK, (GAME_WIDTH, 200), (WIDTH, 200), 2)
        pygame.draw.line(self.screen, BLACK, (GAME_WIDTH, 530), (WIDTH, 530), 2)
        for box in self.tower_box_list:
            box.draw_box(self.screen)

    def draw_upgrade_box(self, upgrade_price):
        self.upgrade_box.draw_box(self.screen, upgrade_price)

    def draw_game_info(self):
        self.health_text = self.text_font.render(f"{str(self.health)}/100", False, BLACK)
        self.money_text = self.text_font.render(str(self.money), False, BLACK)
        self.wave_text = self.text_font.render(f"Wave: {str(self.wave)}", False, BLACK)
        
        self.screen.blit(self.health_surf, self.health_surf_rect)
        self.screen.blit(self.health_text, self.health_text_rect)
        self.screen.blit(self.coin_surf, self.coin_surf_rect)
        self.screen.blit(self.money_text, self.money_text_rect)
        self.screen.blit(self.wave_text, self.wave_text_rect)
    
    def display(self):
        self.draw_tower_boxes()
        self.draw_game_info()

class Box:
    def __init__(self, box_type, pos):
        self.pos = pos
        self.box_type = box_type
        
        if self.box_type != "upgrade":
            self.box_surf = pygame.image.load("../graphics/ui/icon.png").convert_alpha()
            
            if self.box_type == "stone":
                self.projectile_surf = pygame.image.load("../graphics/projectile/stone.png").convert_alpha()
            elif self.box_type == "rock":
                self.projectile_surf = pygame.image.load("../graphics/projectile/rock.png").convert_alpha()
            self.projectile_rect = self.projectile_surf.get_rect(bottomright = pos)
        else:
            self.text_font = pygame.font.Font("../font/ARCADEPI.TTF", 15)
            self.upgrade_text = self.text_font.render("Upgrade(    )", False, BLACK)
            self.upgrade_rect = self.upgrade_text.get_rect(center=pos)

            self.box_surf = pygame.image.load("../graphics/ui/upgrade_icon.png").convert_alpha()
            self.box_surf = pygame.transform.scale(self.box_surf, (UI_WIDTH - 20, self.box_surf.get_height()))
        
        self.rect = self.box_surf.get_rect(center = pos)

    def draw_box(self, surface, upgrade_price=None):
        surface.blit(self.box_surf, self.rect.topleft)
        if self.box_type != "upgrade":
            surface.blit(self.projectile_surf, self.projectile_rect.center)
        else:
            self.upgrade_text = self.text_font.render(f"Upgrade ({str(upgrade_price)})", False, BLACK)
            surface.blit(self.upgrade_text, (self.upgrade_rect))
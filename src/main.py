import pygame, sys
from settings import *
from tile import Tile

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.tile_sprites = pygame.sprite.Group()

        self.setup_map()

    def setup_map(self):
        for row_index, row in enumerate(TILE_MAP):
            y = row_index * TILE_HEIGHT
            for col_index, col in enumerate(row):
                x = col_index * TILE_WIDTH
                Tile(self.tile_sprites, col, (x, y))

    def run(self):
        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.tile_sprites.draw(self.screen)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
# Game window settings
WIDTH = 1500
HEIGHT = 800
GAME_WIDTH = WIDTH - 220
FPS = 60

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (128, 0, 0)
CIRCLE_RED = (255, 0, 0)
CIRCLE_BLUE = (0, 0, 255)

# Tiles settings
TILE_MAP = ["2222222222222222",
            "2222221111122222",
            "2222111222122111",
            "2222122222111122",
            "1111122222222222",
            "2212222222222222",
            "2212221111222211",
            "2211111221221112",
            "2222222221111222",
            "2222222222222222"]

TILE_LEGEND = {"1": "sand_tile",
               "2": "grass_tile_1",
               "3": "grass_tile_2",
               "4": "grass_tile_3"}

TILE_WIDTH = TILE_HEIGHT = 80

# Tower settings
TOWER_RECT_WIDTH = TILE_WIDTH * 3 / 2
TOWER_RECT_HEIGHT = TILE_HEIGHT * 1.8
MAX_RADIUS = 5 * TILE_WIDTH
CIRCLE_ALPHA = 60
UPGRADE_PRICES = {"stone_tower_1": 750,
                  "stone_tower_2": 2000,
                  "rock_tower_1": 1000,
                  "rock_tower_2": 2500}

# Enemy settings
ENEMY_MAX_HEALTH = 100

# UI settings
UI_WIDTH = 220
TOWER_BOX_WIDTH = TOWER_BOX_HEIGHT = UI_WIDTH // 2
# Configurations (USER)
SIZE_SCALE = 1
SPEED_DEFAULT = 750  # 750 MS
SPEED_SCALE_ENABLED = True  # game gets faster with more points?
SPEED_SCALE = 0.05  # speed = max(50, 750 - SCORE * SPEED_SCALE)
DISPLAY_PREDICTION = True
HAS_DISPLAY = True
MIN_DEBUG_LEVEL = 1

FONT_NAME = "Roboto"

COLORS = {
    # Display
    "BACKGROUND_BLACK": "000000",
    "BACKGROUND_DARK": "021c2d",
    "BACKGROUND_LIGHT": "00263f",
    "TRIANGLE_GRAY": "efe6ff",
    "WHITE": "ffffff",
    "RED": "ff0000",
    # Tetris pieces
    "TILE_I_PIECE": "00ffff",
    "TILE_L_PIECE": "ff7f00",
    "TILE_J_PIECE": "0000ff",
    "TILE_S_PIECE": "00ff00",
    "TILE_Z_PIECE": "ff0000",
    "TILE_T_PIECE": "800080",
    "TILE_O_PIECE": "ffff00",
    # Highlights
    "HIGHLIGHT_GREEN": "22ee22",
    "HIGHLIGHT_RED": "ee2222",
}

MESSAGES = {
    # Display
    "TITLE": "Tetris",
    "CONTROLS": "Left/Right - Move tile\nUp - Rotate tile\nDown - Fast drop\nSpace - Insta-drop\nEscape - Play/Pause\nTab - Swap next tile",
    "HIGH_SCORE": "H.Score: {:.2f} (x{})",
    "SCORE": "Score: {:.2f} (x{})",
    "FITNESS": "Fitness: {:.2f}",
    "SPEED": "Speed: {}ms",
    "NEXT_TILE": "Next tile: {}",
}

SEP = ", "


# Configurations (SYSTEM)
GRID_ROW_COUNT = 20
GRID_COL_COUNT = 10

SCREEN_RATIO = 0.55
SCREEN_WIDTH = int(360 / SCREEN_RATIO * SIZE_SCALE)
SCREEN_HEIGHT = int(720 * SIZE_SCALE)
MAX_FPS = 30


########################
# Score Configurations #
########################
MULTI_SCORE_ALGORITHM = lambda lines_cleared: 5 ** lines_cleared
PER_STEP_SCORE_GAIN = 0.001

# "Optimal" fitness function configuration
WEIGHT_AGGREGATE_HEIGHT = -0.3
WEIGHT_HOLES = -0.75
WEIGHT_BUMPINESS = -0.18
WEIGHT_LINE_CLEARED = 1.3

######################
# STEP Configuration #
######################
ALWAYS_DRAW = True
STEP_ACTION = True

ACTIONS = ["NOTHING", "L", "R", "2L", "2R", "ROTATE", "SWAP", "FAST_FALL", "INSTA_FALL"]


######################
# Tile Configuration #
######################
TILES = ["I_PIECE", "L_PIECE", "J_PIECE", "S_PIECE", "Z_PIECE", "T_PIECE", "O_PIECE"]
TILE_SHAPES = {
    "I_PIECE": [[1, 1, 1, 1]],
    "L_PIECE": [[0, 0, 2],
                [2, 2, 2]],
    "J_PIECE": [[3, 0, 0],
                [3, 3, 3]],
    "S_PIECE": [[0, 4, 4],
                [4, 4, 0]],
    "Z_PIECE": [[5, 5, 0],
                [0, 5, 5]],
    "T_PIECE": [[6, 6, 6],
                [0, 6, 0]],
    "O_PIECE": [[7, 7],
                [7, 7]]
} 
"""
This file contains constants used by other files. Constants that should not be modified or automatic constants should be left alone, but the other ones are fine to modify.
"""

# Modifiable Constants
BOARD_DIMENSIONS = (400, 400)  # The size of the screen
GRID_DIMENSIONS = (10, 10)  # The number of tiles in the horizontal and vertical directions
NUMBER_MINES = 10  # The number of mines to be generated on the board
SOLVER_ANIM_DELAY = 0  # How long the solver should wait between moves

# Aesthetical Constants
GREY_PRIMARY = (192, 192, 192)
GREY_SECONDARY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

TILE_PAD = 1  # Default padding so known tiles are simple
TILE_PAD_2 = 3  # Interior padding for mine, flag and thickness of unkown tiles

NUMBER_COLOR_LOOKUP = {'1': (0, 0, 255), '2': (0, 128, 0), '3': (255, 0, 0), '4': (0, 0, 128), '5': (255, 93, 0),
                       '6': (93, 255, 0), '7': (255, 0, 93), '8': (93, 0, 255)}

# Constants that should not be modified
TILE_TEXT_SIZE = 40

# Automatically initialized constants
WINDOW_DIMENSIONS = (BOARD_DIMENSIONS[0], BOARD_DIMENSIONS[1])

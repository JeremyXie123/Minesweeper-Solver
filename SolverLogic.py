import time

from MainProgram import MineSweeperBoard
from BoardTile import BoardTile
from Constants import *


class Solver:
    def __init__(self, game_board: MineSweeperBoard):
        self.game_board = game_board

    def solve_board(self):
        while True and self.game_board.loss is not True:
            tile = self.choose_tile()
            tile.uncover()
            time.sleep(SOLVER_ANIM_DELAY)

    def choose_tile(self) -> BoardTile:
        tiles = self.game_board.get_unknown_tiles()

        # Evaluate the chance of each tile and map it into a dictionary
        tile_score_lookup = dict()
        for tile in tiles:
            curx, cury = tile.id
            tile_score_lookup[tile] = self.evaluate_chance(curx, cury)

        # Invert the lookup dictionary
        score_tile_lookup = {v: k for (k, v) in tile_score_lookup.items()}

        chances = score_tile_lookup.keys()
        best_chance = max(chances)
        return score_tile_lookup[best_chance]

    def evaluate_chance(self, x: int, y: int) -> float:
        """
        Determine the chance that the given tile is safe
        :param x: the x grid coordinate of the desired tile, from left to right
        :param y: the y grid coordinate of the desired tile, from top to bottom
        :return: the probability that the tile does not contain a bomb
        """
        tiles = self.game_board.get_surrounding_tiles(x, y)
        return 0

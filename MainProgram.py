import random

import pygame
import sys

from Constants import *
from BoardTile import BoardTile

# Creating the font
class MineSweeperBoard:
    """
    This class initializes a mine sweeper game on a board and provides various methods to interact with it. The board is represented by a two-dimensional array indexed via [y][x]

    Each tile is indexed in the tile_table 2D array, with the position (x,y) being indexed as tile_table[y][x].

    The position (0,0) represents the top left tile, while (x,y) represents a tile placed x right and y down.
    """

    def __init__(self):
        """Initializes a MineSweeperBoard object"""
        # Initializing the window
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
        self.screen.fill(WHITE)
        pygame.display.set_caption('PyMineSweeper')

        self.font = pygame.font.SysFont('lucidaconsole', TILE_TEXT_SIZE)  # Font for numbers in squares

        # Initialize objects for
        self.tile_table = [[None for x in range(GRID_DIMENSIONS[0])] for y in range(GRID_DIMENSIONS[1])]

        tile_dim = (BOARD_DIMENSIONS[0] // GRID_DIMENSIONS[0], BOARD_DIMENSIONS[1] // GRID_DIMENSIONS[1])

        self.mine_tiles = []
        for i in range(NUMBER_MINES):
            x = random.randint(0, GRID_DIMENSIONS[0] - 1)
            y = random.randint(0, GRID_DIMENSIONS[1] - 1)
            tile = BoardTile(self.screen, self, (x, y),
                                              (x * tile_dim[0], y * tile_dim[1]), tile_dim, self.font,
                                              "mine")
            self.tile_table[y][x] = tile
            self.mine_tiles.append(tile)

        for x in range(0, GRID_DIMENSIONS[0]):
            for y in range(0, GRID_DIMENSIONS[1]):
                if self.tile_table[y][x] is None:
                    self.tile_table[y][x] = BoardTile(self.screen, self, (x, y),
                                                      (x * tile_dim[0], y * tile_dim[1]), tile_dim,
                                                      self.font, "number")

        self.flags_left = NUMBER_MINES

        # Mainloop
        while True:
            # Drawing tiles on the board
            for x in range(0, GRID_DIMENSIONS[0]):
                for y in range(0, GRID_DIMENSIONS[1]):
                    self.tile_table[y][x].render_tile()

            # Code to exit the program if the quit button is pressed
            for event in pygame.event.get():  # Quitting when the exit button is pressed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Behaviour when the left/right mouse is clicked
                    mx, my = pygame.mouse.get_pos()
                    for x in range(0, GRID_DIMENSIONS[0]):
                        for y in range(0, GRID_DIMENSIONS[1]):
                            self.tile_table[y][x].on_clicked(mx, my, event.button)
                    if self.check_win():
                        print("Winner!")

            pygame.display.update()

    def get_surrounding_tiles(self, x: int, y: int) -> list[BoardTile]:
        """
        Returns the tiles surrounding a given tile.

        :param x: the x grid coordinate of the desired tile, from left to right
        :param y: the y grid coordinate of the desired tile, from top to bottom
        :return: an array containing the surrounding tiles
        """
        tiles = []
        # Check all tiles around the current tile (8 in total)
        for a, b in [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]:
            cur_x = x + a
            cur_y = y + b
            # Only check squares INSIDE the board (matters at the edges)
            if 0 <= cur_x <= GRID_DIMENSIONS[0] - 1 and 0 <= cur_y <= GRID_DIMENSIONS[1] - 1:
                temp = self.tile_table[cur_y][cur_x]
                if temp is not None:  # Small check because bombs are initialized first and then the tiles randomly
                    tiles.append(temp)
        return tiles

    def get_surrounding_mines(self, x: int, y: int) -> int:
        """
        Returns the number of mines surrounding the current tile

        :param x: the x grid coordinate of the desired tile, from left to right
        :param y: the y grid coordinate of the desired tile, from top to bottom
        :return: the number of mines surrounding the current tile
        """
        count = 0
        tiles = self.get_surrounding_tiles(x, y)
        for tile in tiles:
            if tile.true_type == "mine":
                count += 1
        return count

    def uncover_neighbouring(self, x: int, y: int, visited: set[BoardTile]) -> None:
        """
        Uncovers the tiles surrounding a given tile

        :param x: the x grid coordinate of the current tile, from left to right
        :param y: the y grid coordinate of the current tile, from top to bottom
        :param visited: a set containing the tiles already visitted during the search.
        This should be set to set() to start a search
        """
        # Perform a recursive search on all neighbours
        cur_tile = self.tile_table[y][x]
        visited.add(cur_tile)

        neighbours = self.get_surrounding_tiles(x, y)
        for tile in neighbours:
            tile.cur_type = tile.true_type
            if tile.true_type == "number" and tile.number == 0 and tile not in visited:
                cur_x, cur_y = tile.id
                self.uncover_neighbouring(cur_x, cur_y, visited)

    def game_over(self) -> None:
        """
        Called when the player clicks on a bomb tile. Currently prints a game over message to the console.
        """
        print("Game Over.")

    def check_win(self) -> bool:
        """
        Checks if you have won (flagged all the tiles containing mines)
        :return: Whether you have won
        """
        count = 0
        for tile in self.mine_tiles:
            if tile.cur_type == "flag" and tile.true_type == "mine":
                count += 1
        return count == NUMBER_MINES

if __name__ == "__main__":
    MineSweeperBoard()

import random

import pygame
import sys

from Constants import *
from BoardTile import BoardTile


# Creating the font
class MineSweeperBoard():
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
        screen.fill(WHITE)
        pygame.display.set_caption('PyMineSweeper')

        font1 = pygame.font.SysFont('lucidaconsole', OPTION_BAR_TEXT_SIZE)  # Font for option bar
        font2 = pygame.font.SysFont('lucidaconsole', TILE_TEXT_SIZE)  # Font for numbers in squares

        # Initialize objects for
        self.tile_table = [[None for x in range(GRID_DIMENSIONS[0])] for y in range(GRID_DIMENSIONS[1])]

        tile_dim = (BOARD_DIMENSIONS[0] // GRID_DIMENSIONS[0], BOARD_DIMENSIONS[1] // GRID_DIMENSIONS[1])

        for i in range(NUMBER_MINES):
            x = random.randint(0, GRID_DIMENSIONS[0] - 1)
            y = random.randint(0, GRID_DIMENSIONS[1] - 1)
            self.tile_table[y][x] = BoardTile(screen, self, (x, y),
                                              (x * tile_dim[0], y * tile_dim[1] + OPTION_BAR_HEIGHT), tile_dim, font2,
                                              "mine")

        for x in range(0, GRID_DIMENSIONS[0]):
            for y in range(0, GRID_DIMENSIONS[1]):
                if self.tile_table[y][x] is None:
                    self.tile_table[y][x] = BoardTile(screen, self, (x, y),
                                                      (x * tile_dim[0], y * tile_dim[1] + OPTION_BAR_HEIGHT), tile_dim,
                                                      font2, "number")

        # Mainloop
        while True:
            # Drawing the option bar
            self.draw_option_bar(screen, font1, 11)

            # Drawing tiles on the board
            for x in range(0, GRID_DIMENSIONS[0]):
                for y in range(0, GRID_DIMENSIONS[1]):
                    self.tile_table[y][x].render_tile()

            # Code to exit the program if the quit button is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    for x in range(0, GRID_DIMENSIONS[0]):
                        for y in range(0, GRID_DIMENSIONS[1]):
                            self.tile_table[y][x].on_clicked(mx, my, event.button)

            pygame.display.update()

    def draw_option_bar(self, screen, font, flags: int) -> None:
        flag_str = "Flags: " + str(flags)
        label1 = font.render(flag_str, True, RED)
        width1, height1 = font.size(flag_str)
        screen.blit(label1, (WINDOW_DIMENSIONS[0] * 1 / 4 - width1 / 2, 20 - height1 / 2))

        solve_str = "Solve"
        label2 = font.render(solve_str, True, RED)
        width2, height2 = font.size(solve_str)
        screen.blit(label2, (WINDOW_DIMENSIONS[0] * 2 / 4 - width2 / 2, 20 - height2 / 2))

        restart_str = "Restart"
        label3 = font.render(restart_str, True, RED)
        width3, height3 = font.size(restart_str)
        screen.blit(label3, (WINDOW_DIMENSIONS[0] * 3 / 4 - width3 / 2, 20 - height3 / 2))
        return

    def get_surrounding_tiles(self, x: int, y: int) -> list[BoardTile]:
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
        count = 0
        tiles = self.get_surrounding_tiles(x, y)
        for tile in tiles:
            if tile.true_type == "mine":
                count += 1
        return count

    def uncover_neighbouring(self, x: int, y: int, visited: set[BoardTile]) -> None:
        # Perform a recursive search on all neighbours
        cur_tile = self.tile_table[y][x]
        visited.add(cur_tile)

        neighbours = self.get_surrounding_tiles(x, y)
        for tile in neighbours:
            if tile.true_type == "number" and tile.number == 0 and tile not in visited:
                tile.cur_type = tile.true_type
                cur_x, cur_y = tile.id
                self.uncover_neighbouring(cur_x, cur_y, visited)

if __name__ == "__main__":
    MineSweeperBoard()

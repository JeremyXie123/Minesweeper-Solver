import pygame

from Constants import *

from MainProgram import MineSweeperBoard


class BoardTile:
    """
    This class represents a tile in the mine sweeper game. It processes interactions with tiles and their rendering.
    """

    def __init__(self, screen: pygame.display, game_board: MineSweeperBoard, id: tuple[int, int], pos: tuple[int, int], size: tuple[int, int], font: pygame.font, type: str):
        """
        Initializes a BoardTile object

        :param screen: the screen to draw onto
        :param game_board: the MineSweeperBoard representing your current board
        :param id: the grid position of the tile on the board
        :param pos: the position of the tile on the screen, based on its pixel coordinates
        :param size: the size of the tile on the screen, based on its pixel coordinates
        :param font: the font used to draw the numbers on the tile
        :param type: the type of tile desired (mine or number)
        """
        self.screen = screen
        self.pos = pos
        self.id = id
        self.size = size
        self.true_type = type
        self.cur_type = "unknown"
        self.font = font
        self.game_board = game_board
        self.number = 0

        if self.true_type == "number":
            self.number = self.game_board.get_surrounding_mines(self.id[0], self.id[1])

    def is_in_tile(self, x, y):
        """
        Returns whether a screen position is within the boundaries of a tile

        :param x: the screen x coordinate of the mouse
        :param y: the screen y coordinate of the mouse
        :return: A boolean representing whether the position is within the tile
        """
        xmin = self.pos[0]
        xmax = self.pos[0] + self.size[0]
        ymin = self.pos[1]
        ymax = self.pos[1] + self.size[1]
        # Check if the mouse is within the boundaries
        if xmin <= x <= xmax and ymin <= y <= ymax:
            return True
        return False

    def on_clicked(self, x: int, y: int, button: pygame.mouse) -> None:
        """
        Defines the behaviour of the tile when clicked by the mouse

        :param x: the screen x coordinate of the mouse
        :param y: the screen y coordinate of the mouse
        :param button: the current mouse pressed (1 for left, 3 for right)
        """
        if self.is_in_tile(x, y):
            if button == 1:  # Left Click
                if self.cur_type != "flag":  # Flagged squares cannot be revealed
                    if self.true_type == "mine":
                        self.game_board.game_over()
                    elif self.true_type == "number" and self.number == 0:
                        # We also want to clear all tiles linked to this one that are empty
                        cur_x, cur_y = self.id
                        self.game_board.uncover_neighbouring(cur_x, cur_y, set())
                    self.cur_type = self.true_type
            elif button == 3:  # Right Click
                # Flips the state of a tile between unknown and flag
                if self.cur_type == "unknown":
                    self.cur_type = "flag"
                elif self.cur_type == "flag":
                    self.cur_type = "unknown"

    def render_tile(self) -> None:
        """
        Renders the tile according to its type and attributes
        """
        if self.cur_type == "unknown":
            rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
            pygame.draw.rect(self.screen, GREY_PRIMARY, rect)

            rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
            pygame.draw.rect(self.screen, GREY_SECONDARY, rect, TILE_PAD)

            # Polygon points for creating the special square design with bevelled corners
            L = self.pos[0] + TILE_PAD  # Represents the x coordinate of the left corners
            R = self.pos[0] + self.size[0] - TILE_PAD  # Represents the x coordinate of the right corners
            U = self.pos[1] + TILE_PAD  # Represents the y coordinate of the upper corners
            D = self.pos[1] + self.size[1] - TILE_PAD  # Represents the y coordinate of the upper corners

            topleft = [(L, U), (R, U),
                       (R - TILE_PAD_2, U + TILE_PAD_2),
                       (L + TILE_PAD_2, U + TILE_PAD_2),
                       (L + TILE_PAD_2, D - TILE_PAD_2),
                       (L, D)]

            bottomright = [(R, D), (R, U),
                           (R - TILE_PAD_2, U + TILE_PAD_2),
                           (R - TILE_PAD_2, D - TILE_PAD_2),
                           (L + TILE_PAD_2, D - TILE_PAD_2),
                           (L, D)]

            pygame.draw.polygon(self.screen, WHITE, topleft)
            pygame.draw.polygon(self.screen, GREY_SECONDARY, bottomright)
        elif self.cur_type == "mine":
            rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
            pygame.draw.rect(self.screen, GREY_PRIMARY, rect)

            rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
            pygame.draw.rect(self.screen, GREY_SECONDARY, rect, TILE_PAD)

            pygame.draw.circle(self.screen, BLACK, (self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2),
                               self.size[0] / 2 - TILE_PAD_2 * 2)
            pygame.draw.circle(self.screen, WHITE, (self.pos[0] + self.size[0] / 2.5, self.pos[1] + self.size[1] / 2.5),
                               self.size[0] / 6 - TILE_PAD_2 * 2)
        elif self.cur_type == "flag":
            rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
            pygame.draw.rect(self.screen, GREY_PRIMARY, rect)

            rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
            pygame.draw.rect(self.screen, GREY_SECONDARY, rect, TILE_PAD)

            points = [(self.pos[0] + TILE_PAD_2, self.pos[1] + self.size[1] / 2),
                      (self.pos[0] + self.size[0] - TILE_PAD_2, self.pos[1] + TILE_PAD_2),
                      (self.pos[0] + self.size[0] - TILE_PAD_2, self.pos[1] + self.size[1] - TILE_PAD_2)]
            pygame.draw.polygon(self.screen, RED, points)
        elif self.cur_type == "number":
            rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
            pygame.draw.rect(self.screen, GREY_PRIMARY, rect)

            rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
            pygame.draw.rect(self.screen, GREY_SECONDARY, rect, TILE_PAD)

            # Rendering the number in the tile
            if self.number != 0:  # We treat number tiles of 0 as blank squares (no digit is drawn)
                number = str(self.number)
                number_color = NUMBER_COLOR_LOOKUP[number]
                number_image = self.font.render(number, True, number_color)
                number_image = pygame.transform.scale(number_image,
                                                      (self.size[0] - 2 * TILE_PAD_2, self.size[1] - 2 * TILE_PAD_2))
                dim = number_image.get_size()
                self.screen.blit(number_image, (self.pos[0] + dim[0] / 10, self.pos[1] + dim[1] / 10))

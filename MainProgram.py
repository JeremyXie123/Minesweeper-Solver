import random

import pygame
import sys

# Modifiable Constants
BOARD_DIMENSIONS = (400, 400)
GRID_DIMENSIONS = (10, 10)

GREY_PRIMARY = (192, 192, 192)
GREY_SECONDARY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

TILE_PAD = 1 # Default padding so known tiles are simple
TILE_PAD_2 = 3 # Interior padding for mine, flag and thickness of unkown tiles

# Constants that should not be modified
OPTION_BAR_HEIGHT = 40
OPTION_BAR_TEXT_SIZE = 20
TILE_TEXT_SIZE = 40

NUMBER_COLOR_LOOKUP = {'1': (0, 0, 255), '2': (0, 128, 0), '3': (255,0,0), '4': (0, 0, 128)}

# Automatically initialized constants
WINDOW_DIMENSIONS = (BOARD_DIMENSIONS[0], BOARD_DIMENSIONS[1]+OPTION_BAR_HEIGHT)

# Creating the font

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    screen.fill(WHITE)
    pygame.display.set_caption('PyMineSweeper')

    font1 = pygame.font.SysFont('lucidaconsole', OPTION_BAR_TEXT_SIZE)  # Font for option bar
    font2 = pygame.font.SysFont('lucidaconsole', TILE_TEXT_SIZE)  # Font for numbers in squares

    # Mainloop
    while True:
        tile_dim = (BOARD_DIMENSIONS[0] // GRID_DIMENSIONS[0], BOARD_DIMENSIONS[1] // GRID_DIMENSIONS[1])

        # Drawing the option bar
        draw_option_bar(screen, font1, 11)

        # Drawing tiles on the board
        for x in range(0, GRID_DIMENSIONS[0]):
            for y in range(0, GRID_DIMENSIONS[1]):
                draw_tile(screen, (x * tile_dim[0], y * tile_dim[1] + OPTION_BAR_HEIGHT), tile_dim, font2, "number")

        # Code to exit the program if the quit button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def draw_option_bar(screen, font, flags):
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

def draw_tile(screen,pos,size,font,type):
    if type == "unfilled":
        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        pygame.draw.rect(screen, GREY_PRIMARY, rect)

        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        pygame.draw.rect(screen, GREY_SECONDARY, rect, TILE_PAD)

        # Polygon points for creating the special square design with bevelled corners
        L = pos[0] + TILE_PAD  # Represents the x coordinate of the left corners
        R = pos[0] + size[0] - TILE_PAD  # Represents the x coordinate of the right corners
        U = pos[1] + TILE_PAD # Represents the y coordinate of the upper corners
        D = pos[1] + size[1] - TILE_PAD # Represents the y coordinate of the upper corners

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

        pygame.draw.polygon(screen, WHITE, topleft)
        pygame.draw.polygon(screen, GREY_SECONDARY, bottomright)
    elif type == "filled":
        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        pygame.draw.rect(screen, GREY_PRIMARY, rect)

        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        pygame.draw.rect(screen, GREY_SECONDARY, rect, TILE_PAD)
    elif type == "mine":
        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        pygame.draw.rect(screen, GREY_PRIMARY, rect)

        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        pygame.draw.rect(screen, GREY_SECONDARY, rect, TILE_PAD)

        pygame.draw.circle(screen, BLACK, (pos[0] + size[0]/2, pos[1] + size[1]/2), size[0]/2 - TILE_PAD_2*2)
        pygame.draw.circle(screen, WHITE, (pos[0] + size[0]/2.5, pos[1] + size[1]/2.5), size[0]/6 - TILE_PAD_2*2)
    elif type == "flag":
        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        pygame.draw.rect(screen, GREY_PRIMARY, rect)

        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        pygame.draw.rect(screen, GREY_SECONDARY, rect, TILE_PAD)

        points = [(pos[0] + TILE_PAD_2, pos[1] + size[1]/2),
                  (pos[0] + size[0] - TILE_PAD_2, pos[1] + TILE_PAD_2),
                  (pos[0] + size[0] - TILE_PAD_2, pos[1] + size[1] - TILE_PAD_2)]
        pygame.draw.polygon(screen, RED, points)
    elif type == "number":
        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        pygame.draw.rect(screen, GREY_PRIMARY, rect)

        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        pygame.draw.rect(screen, GREY_SECONDARY, rect, TILE_PAD)

        # Rendering the number in the tile
        number = str(random.randint(1, 4))
        number_color = NUMBER_COLOR_LOOKUP[number]
        number_image = font.render(number, True, number_color)
        number_image = pygame.transform.scale(number_image, (size[0] - 2*TILE_PAD_2, size[1] - 2*TILE_PAD_2))
        dim = number_image.get_size()
        screen.blit(number_image, (pos[0] + dim[0] / 10, pos[1] + dim[1] / 10))
    return

main()

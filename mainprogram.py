import pygame
import sys

# Initial game constants
PRIMARY = (192, 192, 192)
SECONDARY = (128, 128, 128)
WINDOW_DIMENSIONS = (400, 400)
GRID_DIMENSIONS = (10, 10)


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_DIMENSIONS)
    screen.fill(PRIMARY)

    # Mainloop
    while True:
        tile_dim = (WINDOW_DIMENSIONS[0] // GRID_DIMENSIONS[0], WINDOW_DIMENSIONS[1] // GRID_DIMENSIONS[1])

        for x in range(0, GRID_DIMENSIONS[0]):
            for y in range(0, GRID_DIMENSIONS[1]):
                rect = pygame.Rect(x * tile_dim[0], y * tile_dim[1], tile_dim[0], tile_dim[1])
                pygame.draw.rect(screen, SECONDARY, rect, 1)

        # Code to exit the program if the quit button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


main()

import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import colors
import pygame
from pygame.image import tostring

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)





class Map:
    EMPTY = 0
    OBSTACLE = 1
    START = 2
    GOAL = 3
    TRAVELLED = 10

    def __init__(self, rows, cols):
        self.start_coord = None
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols))

    def __str__(self):
        return self.grid.__str__()

    def set_start(self, start_pos):
        self.grid[start_pos[0], start_pos[1]] = Map.START
        self.start_coord = start_pos

    def set_goal(self, goal_pos):
        self.grid[goal_pos[0], goal_pos[1]] = Map.GOAL

    def set_obstacles(self, obstacle_coords):
        for coord in obstacle_coords:
            self.grid[coord[0], coord[1]] = Map.OBSTACLE

    def _draw_rect(self, grid_coord = (0, 0), color = BLACK, border_size = 1):
        """Draw a rectangle"""
        coord = (grid_coord[0] * self._box_size, grid_coord[1] * self._box_size)
        # Draw border
        pygame.draw.rect(
            self._screen,
            BLACK,
            (coord[1], coord[0], self._box_size, self._box_size),
            )
        # Draw main rectangle
        pygame.draw.rect(
            self._screen,
            color,
            (coord[1] + border_size, coord[0] + border_size, self._box_size - border_size, self._box_size - border_size),
            )

        # Draw font
        font = pygame.font.Font(None, 20)
        text = str(grid_coord)
        text_color = (100, 100, 100)
        text_surface = font.render(text, True, text_color)
        text_coord = (coord[1] + border_size, (coord[0] + border_size))
        self._screen.blit(text_surface, text_coord)

    def _draw_grid(self):
        """Draw grid based on colored rectangles"""
        for row_index, row in enumerate(self.grid):
            for col_index, element in enumerate(row):
                if element == Map.EMPTY:
                    box_color = WHITE
                elif element == Map.OBSTACLE:
                    box_color = BLACK
                elif element == Map.START:
                    box_color = GREEN
                elif element == Map.GOAL:
                    box_color = RED
                else:
                    box_color = YELLOW
                self._draw_rect((row_index, col_index), box_color)


    def visualize(self, screen_width = 500, screen_height = 500):

        pygame.init()
        self._box_size = min(screen_width, screen_height) / max(self.grid.shape) # JUST TEMPORARY
        self._screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Map test")
        self._screen.fill(WHITE)

        self._draw_grid()



        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()
        pygame.quit()

    def _set_coord_value(self, coord, value):
        self.grid[coord[0], coord[1]] = value

    def _get_coord_value(self, coord):
        return self.grid[coord[0], coord[1]]

    def _is_travelable(self, coord):
        # Out of bound
        if not(0 <= coord[0] < self.rows and 0 <= coord[1] < self.cols):
            return False
        # Is obstacle or travelled
        coord_value = self.grid[coord[0], coord[1]]
        if coord_value == Map.OBSTACLE or coord_value == Map.TRAVELLED or coord_value == Map.START:
            return False
        return True

    def _find_neighbors(self, coord):
        """Find neighbors' coords of a coord"""
        row, col = coord[0], coord[1]

        left = (row, col - 1)
        right = (row, col + 1)
        top = (row - 1, col)
        bottom = (row + 1, col)

        neighbors =  [top, left, right, bottom]
        valid_neighbors = []

        for neighbor in neighbors:
            if self._is_travelable(neighbor):
                valid_neighbors.append(neighbor)

        return valid_neighbors

    def dfs_solve(self):
        visited = [self.start_coord]
        stack = []

        while len(visited) > 0:
            current_coord = visited[-1]
            # If found
            if self._get_coord_value(current_coord) == Map.GOAL:
                break

            # Marked as TRAVELLED

            self._set_coord_value(current_coord, Map.TRAVELLED)

            # Find valid neighbors
            neighbors = self._find_neighbors(current_coord)

            # If no neighbors, pop that visited and continue
            if len(neighbors) == 0:
                visited.pop()
                continue

            # Append neighbors
            stack = stack + neighbors

            # Pop the stack to visited
            visited.append(stack.pop())

        return visited


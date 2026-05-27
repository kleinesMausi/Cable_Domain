import pygame
import array
from constants import *

class Grid:
    def __init__(self, grid_height, grid_width):
        self.grid = array.array('B', [States.EMPTY] * (grid_height * grid_width))

        self.grid_height = grid_height
        self.grid_width = grid_width

        self.active_list = set()

        self.sim_speed = 100
        self.sim_timer = 0

    def update(self, dt):
        self.sim_timer += dt
        if self.sim_timer >= self.sim_speed:
            self.sim_timer = 0

            next_grid_changes = {}
            candidates = {}

            for x, y in list(self.active_list):
                cur_state = self.get_grid_at(x, y)

                if cur_state == States.TAIL:
                    next_grid_changes[(x, y)] = States.CABLE

                elif cur_state == States.ELECTRO:
                    next_grid_changes[(x, y)] = States.TAIL

                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            if dx == 0 and dy == 0:
                                continue

                            nx, ny = x + dx, y + dy

                            if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                                if self.get_grid_at(nx, ny) == States.CABLE:
                                    candidates[(nx, ny)] = candidates.get((nx, ny), 0) + 1

            for (x, y), head_count in candidates.items():
                if 0 < head_count <= 2:
                    next_grid_changes[(x, y)] = States.ELECTRO
            
            self.active_list.clear()

            for (x, y), new_val in next_grid_changes.items():
                self.set_grid_at(x, y, new_val)
                if new_val in (States.ELECTRO, States.TAIL):
                    self.active_list.add((x, y))

    def draw(
            self, 
            surface, 
            camera, 
            scaled_cell, 
            rect_size, 
            visibility_scale, 
            grid_width,
            grid_height
            ):

        start_col, end_col, start_row, end_row = camera.get_visibility_range(scaled_cell)
        
        for x in range(max(0, start_col), min(grid_width, end_col)):
            for y in range(max(0, start_row), min(grid_height, end_row)):
                
                screen_x = x * scaled_cell - camera.camera_x
                screen_y = y * scaled_cell - camera.camera_y
                
                cell_state = self.get_grid_at(x, y)

                if cell_state == States.CABLE:
                    pygame.draw.rect(surface, Colors.CABLE, (screen_x, screen_y, rect_size, rect_size))
                elif cell_state == States.TAIL:
                    pygame.draw.rect(surface, Colors.TAIL, (screen_x, screen_y, rect_size, rect_size))
                elif cell_state == States.ELECTRO:
                    pygame.draw.rect(surface, Colors.ELECTRO, (screen_x, screen_y, rect_size, rect_size))
                else:
                    if visibility_scale > 40: 
                        pygame.draw.rect(surface, Colors.GRID, (screen_x, screen_y, int(scaled_cell), int(scaled_cell)), 1)
    
    def set_grid_at(self, x, y, val):
        self.grid[x * self.grid_height + y] = val

    def get_grid_at(self, x, y):
        return self.grid[x * self.grid_height + y]

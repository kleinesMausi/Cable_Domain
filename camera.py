import pygame

class Camera:
    def __init__(self, screen_height, screen_width):
        self.camera_x = 0
        self.camera_y = 0
        self.scroll_speed = 15

        self.screen_height = screen_height
        self.screen_width = screen_width

    def update(self, keys, grid_height, grid_width, cell_size):

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  self.camera_x -= self.scroll_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.camera_x += self.scroll_speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:    self.camera_y -= self.scroll_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  self.camera_y += self.scroll_speed

        max_x = max(0, grid_width * cell_size - self.screen_width)
        max_y = max(0, grid_height * cell_size - self.screen_height)   
  
        self.camera_x = max(0, min(self.camera_x, max_x))
        self.camera_y = max(0, min(self.camera_y, max_y))

    def get_visibility_range(self, scaled_cell):
        start_col = int(self.camera_x // scaled_cell)
        end_col = int((self.camera_x + self.screen_width) // scaled_cell + 1)
        start_row = int(self.camera_y // scaled_cell)
        end_row = int((self.camera_y + self.screen_height) // scaled_cell + 1)

        return start_col, end_col, start_row, end_row
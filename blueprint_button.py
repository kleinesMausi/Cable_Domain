import pygame


class BlueprintButton:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.rect = pygame.Rect(0, 0, 180, 30)

    def draw(self, surface, x, y, font):
        self.rect.topleft = (x, y)
        pygame.draw.rect(surface, (60, 60, 60), self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 1)
        
        txt_surf = font.render(self.name, True, (255, 255, 255))
        surface.blit(txt_surf, (x + 5, y + 5))

    def is_clicked(self, mouse_pos, y_offset):
        screen_rect = self.rect.copy()
        screen_rect.y += y_offset 
        return screen_rect.collidepoint(mouse_pos)

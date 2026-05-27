import pygame


class ToolButton:
    def __init__(self, x, y, width, height, text, color, action_val):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action_val = action_val 

    def draw(self, surface, font):

        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2) 
        
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

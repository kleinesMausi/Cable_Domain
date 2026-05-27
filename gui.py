from tool_button import ToolButton
from constants import *
import pygame 

class Gui:
    def __init__(self, screen_height, screen_width):

        self.screen_height = screen_height

        self.is_visible = False
        self.can_click = False
        self.width = 200
        self.sidebar_rect = pygame.Rect(0, 0, self.width, screen_height)
        
        self.toggle_button = pygame.Rect(10, 10, 40, 40) 

        self.font = pygame.font.SysFont("Arial", 18)

        self.input_text = ""
        self.is_naming = False  
        self.naming_rect = pygame.Rect(
            screen_width // 4, 
            screen_height // 4,
            screen_width // 2,
            screen_height // 2, 
            )
        self.quit_button = pygame.Rect(
            self.naming_rect.left + 25, 
            self.naming_rect.bottom - 100, 
            75, 
            75
            )
        self.input_box = pygame.Rect(
            self.naming_rect.x + 20, 
            self.naming_rect.y + 60, 
            self.naming_rect.width - 40, 
            40
            )
        
        self.tool_buttons = {
            "Cable": ToolButton(
                x = 10,
                y = 60, 
                width = 180,
                height = 40,
                text = "Cable",
                color = (0, 0, 0),
                action_val = States.CABLE
            ),
            "Tail": ToolButton(
                x = 10,
                y = 110, 
                width = 180,
                height = 40,
                text = "Tail",
                color = (0, 0, 0),
                action_val = States.TAIL
            ),
            "Electro": ToolButton(
                x = 10,
                y = 160, 
                width = 180,
                height = 40,
                text = "Electro",
                color = (0, 0, 0),
                action_val = States.ELECTRO
            ),
            "Select": ToolButton(
                x = 10,
                y = 210, 
                width = 180,
                height = 40,
                text = "Select",
                color = (0, 0, 0),
                action_val = States.SELECT
            ),
            "Pase": ToolButton(
                x = 10,
                y = 260, 
                width = 180,
                height = 40,
                text = "Paste",
                color = (0, 0, 0),
                action_val = States.PASTE
            )
        }

        self.blueprint_buttons = []
        self.scroll_offset = 0

    def draw(self, surface, amount_blueprints):

        color_toggle = (0, 255, 0) if self.is_visible else (255, 0, 0)
        
        if self.is_visible:

            pygame.draw.rect(surface, (40, 40, 40), self.sidebar_rect)

            for button in self.tool_buttons.values():
                button.draw(surface = surface, font = self.font)

            list_area_rect = pygame.Rect(0, 310, 200, self.screen_height - 310) 
            list_subsurface = surface.subsurface(list_area_rect)

            for i, button in enumerate(self.blueprint_buttons):
                y_pos = i * 40 - self.scroll_offset 
                button.draw(list_subsurface, 5, y_pos, self.font)

        pygame.draw.rect(surface, color_toggle, self.toggle_button)

  

        if self.is_naming:
            # Gesamt hintergrund Transparent machen (also so ein dunklen/schwarzen schleier drüber)
            overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) 
            surface.blit(overlay, (0, 0))

            pygame.draw.rect(surface, (50, 50, 50), self.naming_rect)
            pygame.draw.rect(surface, (200, 200, 200), self.naming_rect, 2)

            title_surf = self.font.render("Save Blueprint As:", True, (255, 255, 255))
            surface.blit(title_surf, (self.naming_rect.x + 20, self.naming_rect.y + 20))

            pygame.draw.rect(surface, (30, 30, 30), self.input_box)

            pygame.draw.rect(surface, (187, 67, 42), self.quit_button)
            
            text_color = (111,111,111) if self.input_text == "" else (0, 255, 0)
            display_text = f"Blueprint {amount_blueprints + 1}" if self.input_text == "" else self.input_text
            txt_surf = self.font.render(display_text + "|", True, text_color) # | als curser, weil hacker mans
            surface.blit(txt_surf, (self.input_box.x + 5, self.input_box.y + 10))

    def update(self, mouse_pos, mouse_buttons):

        response = {"tool": None, "blueprint": None}

        if not mouse_buttons[0]:
            self.can_click = True

        if self.can_click and mouse_buttons[0] and self.toggle_button.collidepoint(mouse_pos):
            self.is_visible = not self.is_visible
            self.can_click = False

        if self.is_naming and self.can_click and mouse_buttons[0] and self.quit_button.collidepoint(mouse_pos):
            self.is_naming = not self.is_naming
            self.can_click = False
            self.input_text = ""
                

        for blue_button in self.blueprint_buttons:
            if self.can_click and mouse_buttons[0] and blue_button.is_clicked(mouse_pos, y_offset = 310):
                response["blueprint"] = blue_button.data
                response["tool"] = States.PASTE 
                self.can_click = False
                
        if self.is_visible:
            for button in self.tool_buttons.values():
                if self.can_click and mouse_buttons[0] and button.is_clicked(mouse_pos):
                    response["tool"] = button.action_val
                    self.can_click = False
                    break
                
        return response

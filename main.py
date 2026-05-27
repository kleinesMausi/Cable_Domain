from blueprint_button import BlueprintButton
from tool_button import ToolButton
from camera import Camera
from constants import *
from grid import Grid
from gui import Gui

import pygame

# y offset in gui.py is still pretty much unused (scrollinng through mutliple blueprints, if they dont fit on the subsurface anymore)
# Some stuff is still just rando magic numbers, Fix that
# most likely a lot of intertwined logic, that can massively be entangled
# MAKE F****** PERSISTANT MEMORY YOU DUMB ****


class Main:
    def __init__(self, screen_width, screen_height, grid_height, grid_width):
        self.is_running = True
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.screen_height = screen_height
        self.screen_width = screen_width

        self.cell_size = 20
        self.scaled_cell = 20
        self.visibility_scale = 100

        self.cam = Camera(screen_height = self.screen_height, screen_width = self.screen_width)
        self.domain = Grid(self.grid_height, self.grid_width)
        self.gui = Gui(self.screen_height, self.screen_width)
        self.is_paused = True
        self.current_tool = States.CABLE

        self.blueprints = {} # {"name": [...]}
        self.select_start = None
        self.select_end = None
        self.saved_blueprint = None  # Liste von (rel_x, rel_y, wert)
        self.save_electro = False

        self.surface = pygame.display.set_mode((screen_width, screen_height))

    def update(self, keys, dt, mouse_pos, mouse_buttons):
        if not self.gui.is_naming:
            self.cam.update(
                keys = keys,
                grid_height = self.grid_height,
                grid_width = self.grid_width,
                cell_size = self.scaled_cell
            )

        if not self.is_paused:
            self.domain.update(
                dt = dt
            )

        response = self.gui.update(mouse_pos, mouse_buttons)

        if response["tool"] is not None:
            self.current_tool = response["tool"]

        if response["blueprint"] is not None:
            self.saved_blueprint = response["blueprint"]

    def draw(self, rect_size):
        self.surface.fill(Colors.BG)

        self.domain.draw(
            surface = self.surface, 
            camera = self.cam,
            scaled_cell = self.scaled_cell,
            rect_size = rect_size,
            visibility_scale = self.visibility_scale,
            grid_width = self.grid_width,
            grid_height = self.grid_height
        )

                    
        if self.current_tool == States.SELECT and self.select_start and self.select_end:
            x1 = min(self.select_start[0], self.select_end[0]) * self.scaled_cell - self.cam.camera_x
            y1 = min(self.select_start[1], self.select_end[1]) * self.scaled_cell - self.cam.camera_y
            x2 = (max(self.select_start[0], self.select_end[0]) + 1) * self.scaled_cell - self.cam.camera_x
            y2 = (max(self.select_start[1], self.select_end[1]) + 1) * self.scaled_cell - self.cam.camera_y
            
            if x2 - x1 > 0 and y2 - y1 > 0:
                s = pygame.Surface((x2 - x1, y2 - y1), pygame.SRCALPHA)
                s.fill(Colors.SELECT_BOX)
                self.surface.blit(s, (x1, y1))
            
        if self.current_tool == States.PASTE and self.saved_blueprint:
            mx, my = pygame.mouse.get_pos()
            gx = int((mx + self.cam.camera_x) // self.scaled_cell)
            gy = int((my + self.cam.camera_y) // self.scaled_cell)
            
            for rx, ry, val in self.saved_blueprint:
                sx = (gx + rx) * self.scaled_cell - self.cam.camera_x
                sx_y = (gy + ry) * self.scaled_cell - self.cam.camera_y
            
                if self.save_electro:
                     
                    if val == States.CABLE: color = Colors.CABLE
                    if val == States.TAIL: color = Colors.TAIL
                    if val == States.ELECTRO: color = Colors.ELECTRO
                     
                else:color = Colors.CABLE

                pygame.draw.rect(self.surface, color, (sx, sx_y, rect_size, rect_size))
                pygame.draw.rect(self.surface, (255,255,255), (sx, sx_y, rect_size, rect_size), 1)

        self.gui.draw(surface = self.surface, amount_blueprints = len(self.blueprints.keys()))

    def save_current_blueprint(self):
        name = self.gui.input_text.strip()
        amount = len(self.blueprints.keys())

        if name == "":
            name = f"Blueprint {amount + 1}"
        
        if name in self.blueprints:
            name += f" ({amount + 1})" 
            
        self.blueprints[name] = self.saved_blueprint
        self.gui.blueprint_buttons.append(BlueprintButton(name, self.saved_blueprint))
        self.gui.is_naming = False
        self.gui.input_text = ""

    def handle_input(self, keys):

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.is_running = False

            if event.type == pygame.KEYDOWN:

                if self.gui.is_naming:
                    if event.key == pygame.K_BACKSPACE:
                        self.gui.input_text = self.gui.input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.save_current_blueprint()
                    elif len(self.gui.input_text) < 25:
                        self.gui.input_text += event.unicode

                if (event.key == pygame.K_k
                    and 
                    self.saved_blueprint is not None
                    and 
                    self.current_tool == States.PASTE
                    ):
                    self.gui.is_naming = True
                    self.is_paused = True

                if event.key == pygame.K_SPACE:
                    self.is_paused = not self.is_paused

                if event.key == pygame.K_e:
                    self.save_electro = not self.save_electro

                if event.key == pygame.K_1: self.current_tool = States.CABLE
                if event.key == pygame.K_2: self.current_tool = States.TAIL
                if event.key == pygame.K_3: self.current_tool = States.ELECTRO
                if event.key == pygame.K_4: self.current_tool = States.SELECT
                if event.key == pygame.K_5: self.current_tool = States.PASTE

                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:

                    if event.key == pygame.K_MINUS:
                        self.visibility_scale = max(25, self.visibility_scale - 5)

                    elif event.key == pygame.K_PLUS: 
                        self.visibility_scale = min(250, self.visibility_scale + 5)


            if event.type == pygame.MOUSEBUTTONUP:
                # 1 -> Linksklick (halt nur hoch, also nicht klick
                #                  sondern maybe Linksreleas?)
                if event.button == 1 and self.current_tool == States.SELECT:
                    if self.select_start and self.select_end:

                        x1 = min(self.select_start[0], self.select_end[0])
                        y1 = min(self.select_start[1], self.select_end[1])
                        x2 = max(self.select_start[0], self.select_end[0])
                        y2 = max(self.select_start[1], self.select_end[1])
                        
                        # Blaupause (relativ zur oberen linken Ecke x1, y1)
                        self.saved_blueprint = []
                        for x in range(x1, x2 + 1):
                            for y in range(y1, y2 + 1):
                                val = self.domain.get_grid_at(x, y)
                                if val != States.EMPTY:
                                    self.saved_blueprint.append((x - x1, y - y1, val))
                        
                        self.current_tool = States.PASTE
                    
                    self.select_start = None
                    self.select_end = None

    def handle_blueprint(self, grid_x, grid_y):
        if self.current_tool == States.SELECT:

            if self.select_start is None:
                self.select_start = (grid_x, grid_y)

            self.select_end = (grid_x, grid_y)

            return True
            
        elif self.current_tool == States.PASTE:
            if self.saved_blueprint:
                for relative_x, relative_y, val in self.saved_blueprint:
                    true_x, true_y = grid_x + relative_x, grid_y + relative_y

                    if 0 <= true_x < self.grid_width and 0 <= true_y < self.grid_height:

                        if not self.save_electro and val in (States.ELECTRO, States.TAIL): 
                            val = States.CABLE
                            self.domain.active_list.discard((true_x, true_y))

                        self.domain.set_grid_at(true_x, true_y, val)

                        if self.save_electro:
                            self.domain.active_list.add((true_x, true_y))
            
            return True
        
        return False

    def handle_placement(self, mouse_x, mouse_y, mouse_buttons):

        if self.gui.is_visible and self.gui.sidebar_rect.collidepoint((mouse_x, mouse_y)):
            return
        
        if self.gui.toggle_button.collidepoint((mouse_x, mouse_y)):
            return
        
        if self.gui.is_naming:
            return


        real_x = mouse_x + self.cam.camera_x
        real_y = mouse_y + self.cam.camera_y
        
        grid_x = int(real_x // self.scaled_cell)
        grid_y = int(real_y // self.scaled_cell)

        if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
            if mouse_buttons[0]: # Linksklick (setzen)
                
                if not self.handle_blueprint(grid_x = grid_x, grid_y = grid_y):

                    self.domain.set_grid_at(grid_x, grid_y, self.current_tool)

                    if self.current_tool in (States.ELECTRO, States.TAIL):
                        self.domain.active_list.add((grid_x, grid_y))

            elif mouse_buttons[2]: # Rechtsklick (Löschen)
                self.domain.set_grid_at(grid_x, grid_y, States.EMPTY)
                self.domain.active_list.discard((grid_x, grid_y))


    def _set_caption(self):
        if self.is_paused:
            pygame.display.set_caption(f"Cable Domain - PAUSED (Tool: {MINI_TRANS[self.current_tool]} | Speicher Electro: {self.save_electro})")
        else:
            pygame.display.set_caption(f"Cable Domain - RUNNING (Active Electrons: {len(self.domain.active_list)} | Speicher Electro: {self.save_electro})")



def main():
    screen_height = 600
    screen_width = 800
    grid_height = 500
    grid_width = 4000

    pygame.init()    
    clock = pygame.time.Clock()

    control_freak = Main(
        screen_height = screen_height, 
        screen_width = screen_width,
        grid_height = grid_height,
        grid_width = grid_width
    )
    

    while control_freak.is_running:
        dt = clock.tick(60)
        keys = pygame.key.get_pressed()
        control_freak._set_caption()

        scale = control_freak.visibility_scale / 100
        control_freak.scaled_cell = control_freak.cell_size * scale
        rect_size = max(1, int(control_freak.scaled_cell - 1))
        
        control_freak.handle_input(keys = keys)

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        control_freak.update(
            keys = keys, 
            dt = dt, 
            mouse_pos = (mouse_x, mouse_y),
            mouse_buttons = mouse_buttons
            )
        
        control_freak.handle_placement(
            mouse_x = mouse_x,
            mouse_y = mouse_y,
            mouse_buttons = mouse_buttons
        )
        
        control_freak.draw(rect_size)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
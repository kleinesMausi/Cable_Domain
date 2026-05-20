import pygame

EMPTY = 0
CABLE = 1
TAIL = 2
ELECTRO = 3
SELECT = 4 
PASTE = 5   

COLOR_BG = (15, 15, 15)
COLOR_GRID = (30, 30, 30)
COLOR_CABLE = (197, 106, 57)
COLOR_TAIL = (137, 55, 39)
COLOR_ELECTRO = (241, 196, 15)
COLOR_SELECT_BOX = (52, 152, 219, 100) # vierter wert für transparenz, lol

mini_trans = {
    EMPTY : "Empty Cell",
    CABLE : "Cable",
    TAIL : "Tail",
    ELECTRO : "Electro",
    SELECT: "Select Area",
    PASTE: "Paste Blueprint"
}

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

        self.cam = Camera()
        self.domain = Grid(self.grid_height, self.grid_width)
        self.is_paused = True
        self.current_tool = CABLE

        self.select_start = None  # (grid_x, grid_y) beim ersten Klick
        self.select_end = None    # (grid_x, grid_y) beim Ziehen
        self.saved_blueprint = None  # Liste von (rel_x, rel_y, wert)
        self.save_electro = False

        self.surface = pygame.display.set_mode((screen_width, screen_height))

    def update(self, keys, dt):
        self.cam.update(
            keys = keys,
            grid_height = self.grid_height,
            grid_width = self.grid_width,
            screen_height = self.screen_height,
            screen_width = self.screen_width,
            cell_size = self.scaled_cell
        )
        if not self.is_paused:
            self.domain.update(
                dt = dt,
                grid_height = self.grid_height,
                grid_width = self.grid_width
            )

    def draw(self, rect_size):
        self.surface.fill(COLOR_BG)

        start_col = int(self.cam.camera_x // self.scaled_cell)
        end_col = int((self.cam.camera_x + self.screen_width) // self.scaled_cell + 1)
        start_row = int(self.cam.camera_y // self.scaled_cell)
        end_row = int((self.cam.camera_y + self.screen_height) // self.scaled_cell + 1)
        
        for x in range(max(0, start_col), min(self.grid_width, end_col)):
            for y in range(max(0, start_row), min(self.grid_height, end_row)):
                
                screen_x = x * self.scaled_cell - self.cam.camera_x
                screen_y = y * self.scaled_cell - self.cam.camera_y
                
                cell_state = self.domain.grid[x][y]

                if cell_state == CABLE:
                    pygame.draw.rect(self.surface, COLOR_CABLE, (screen_x, screen_y, rect_size, rect_size))
                elif cell_state == TAIL:
                    pygame.draw.rect(self.surface, COLOR_TAIL, (screen_x, screen_y, rect_size, rect_size))
                elif cell_state == ELECTRO:
                    pygame.draw.rect(self.surface, COLOR_ELECTRO, (screen_x, screen_y, rect_size, rect_size))
                else:
                    if self.visibility_scale > 40: 
                        pygame.draw.rect(self.surface, COLOR_GRID, (screen_x, screen_y, int(self.scaled_cell), int(self.scaled_cell)), 1)
                    
        if self.current_tool == SELECT and self.select_start and self.select_end:
            x1 = min(self.select_start[0], self.select_end[0]) * self.scaled_cell - self.cam.camera_x
            y1 = min(self.select_start[1], self.select_end[1]) * self.scaled_cell - self.cam.camera_y
            x2 = (max(self.select_start[0], self.select_end[0]) + 1) * self.scaled_cell - self.cam.camera_x
            y2 = (max(self.select_start[1], self.select_end[1]) + 1) * self.scaled_cell - self.cam.camera_y
            
            if x2 - x1 > 0 and y2 - y1 > 0:
                s = pygame.Surface((x2 - x1, y2 - y1), pygame.SRCALPHA)
                s.fill(COLOR_SELECT_BOX)
                self.surface.blit(s, (x1, y1))
            
        if self.current_tool == PASTE and self.saved_blueprint:
            mx, my = pygame.mouse.get_pos()
            gx = int((mx + self.cam.camera_x) // self.scaled_cell)
            gy = int((my + self.cam.camera_y) // self.scaled_cell)
            
            for rx, ry, val in self.saved_blueprint:
                sx = (gx + rx) * self.scaled_cell - self.cam.camera_x
                sx_y = (gy + ry) * self.scaled_cell - self.cam.camera_y
            
                if self.save_electro:
                     
                    if val == CABLE: color = COLOR_CABLE
                    if val == TAIL: color = COLOR_TAIL
                    if val == ELECTRO: color = COLOR_ELECTRO
                     
                else:color = COLOR_CABLE

                pygame.draw.rect(self.surface, color, (sx, sx_y, rect_size, rect_size))
                pygame.draw.rect(self.surface, (255,255,255), (sx, sx_y, rect_size, rect_size), 1)

    def _set_caption(self):
        if self.is_paused:
            pygame.display.set_caption(f"Cable Domain - PAUSED (Tool: {mini_trans[self.current_tool]} | Speicher Electro: {self.save_electro})")
        else:
            pygame.display.set_caption(f"Cable Domain - RUNNING (Active Electrons: {len(self.domain.active_list)} | Speicher Electro: {self.save_electro})")

class Camera:
    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0
        self.scroll_speed = 15

    def update(self, keys, grid_height, grid_width, screen_height, screen_width, cell_size):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  self.camera_x -= self.scroll_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.camera_x += self.scroll_speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:    self.camera_y -= self.scroll_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  self.camera_y += self.scroll_speed
        
        max_x = max(0, grid_width * cell_size - screen_width)
        max_y = max(0, grid_height * cell_size - screen_height)

        self.camera_x = max(0, min(self.camera_x, max_x))
        self.camera_y = max(0, min(self.camera_y, max_y))

class Grid:
    def __init__(self, grid_height, grid_width):
        self.grid = [[EMPTY for _ in range(grid_height)] for _ in range(grid_width)]
        self.active_list = set()
        self.sim_speed = 100
        self.sim_timer = 0

    def update(self, dt, grid_height, grid_width):
        self.sim_timer += dt
        if self.sim_timer >= self.sim_speed:
            self.sim_timer = 0

            next_grid_changes = {}
            candidates = {}

            for x, y in list(self.active_list):
                cur_state = self.grid[x][y]

                if cur_state == TAIL:
                    next_grid_changes[(x, y)] = CABLE

                elif cur_state == ELECTRO:
                    next_grid_changes[(x, y)] = TAIL

                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            if dx == 0 and dy == 0:
                                continue

                            nx, ny = x + dx, y + dy

                            if 0 <= nx < grid_width and 0 <= ny < grid_height:
                                if self.grid[nx][ny] == CABLE:
                                    candidates[(nx, ny)] = candidates.get((nx, ny), 0) + 1

            for (x, y), head_count in candidates.items():
                if 0 < head_count <= 2:
                    next_grid_changes[(x, y)] = ELECTRO
            
            self.active_list.clear()

            for (x, y), new_val in next_grid_changes.items():
                self.grid[x][y] = new_val
                if new_val in (ELECTRO, TAIL):
                    self.active_list.add((x, y))


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
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                control_freak.is_running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    control_freak.is_paused = not control_freak.is_paused

                if event.key == pygame.K_e:
                    control_freak.save_electro = not control_freak.save_electro

                if event.key == pygame.K_1: control_freak.current_tool = CABLE
                if event.key == pygame.K_2: control_freak.current_tool = TAIL
                if event.key == pygame.K_3: control_freak.current_tool = ELECTRO
                if event.key == pygame.K_4: control_freak.current_tool = SELECT
                if event.key == pygame.K_5: control_freak.current_tool = PASTE

                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:

                    if event.key == pygame.K_MINUS:
                        control_freak.visibility_scale = max(25, control_freak.visibility_scale - 5)

                    elif event.key == pygame.K_PLUS: 
                        control_freak.visibility_scale = min(250, control_freak.visibility_scale + 5)


            if event.type == pygame.MOUSEBUTTONUP:
                # 1 -> Linksklick (halt nur hoch, also nicht klick
                #                  sondern maybe Linksreleas?)
                if event.button == 1 and control_freak.current_tool == SELECT:
                    if control_freak.select_start and control_freak.select_end:

                        x1 = min(control_freak.select_start[0], control_freak.select_end[0])
                        y1 = min(control_freak.select_start[1], control_freak.select_end[1])
                        x2 = max(control_freak.select_start[0], control_freak.select_end[0])
                        y2 = max(control_freak.select_start[1], control_freak.select_end[1])
                        
                        # Blaupause (relativ zur oberen linken Ecke x1, y1)
                        blueprint = []
                        for x in range(x1, x2 + 1):
                            for y in range(y1, y2 + 1):
                                val = control_freak.domain.grid[x][y]
                                if val != EMPTY:
                                    blueprint.append((x - x1, y - y1, val))
                        
                        control_freak.saved_blueprint = blueprint
                        print(f"[Blueprint] Gespeichert! {len(blueprint)} Zellen kopiert.")
                        
                        control_freak.current_tool = PASTE
                    
                    control_freak.select_start = None
                    control_freak.select_end = None

        control_freak.update(keys = keys, dt = dt)
        
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        real_x = mouse_x + control_freak.cam.camera_x
        real_y = mouse_y + control_freak.cam.camera_y
        
        grid_x = int(real_x // control_freak.scaled_cell)
        grid_y = int(real_y // control_freak.scaled_cell)

        if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
            if mouse_buttons[0]: # Linksklick (setzen)
                
                if control_freak.current_tool == SELECT:

                    if control_freak.select_start is None:
                        control_freak.select_start = (grid_x, grid_y)

                    control_freak.select_end = (grid_x, grid_y)
                    
                elif control_freak.current_tool == PASTE:
                    if control_freak.saved_blueprint:
                        for rx, ry, val in control_freak.saved_blueprint:
                            tx, ty = grid_x + rx, grid_y + ry

                            if 0 <= tx < grid_width and 0 <= ty < grid_height:
                                # Strom soll nicht mit!!!!
                                if not control_freak.save_electro and val in (ELECTRO, TAIL): 
                                    val = CABLE
                                    control_freak.domain.active_list.discard((tx, ty))

                                control_freak.domain.grid[tx][ty] = val

                                if control_freak.save_electro:
                                    control_freak.domain.active_list.add((tx, ty))
                else: 
                    control_freak.domain.grid[grid_x][grid_y] = control_freak.current_tool

                    if control_freak.current_tool in (ELECTRO, TAIL):
                        control_freak.domain.active_list.add((grid_x, grid_y))

            elif mouse_buttons[2]: # Rechtsklick (Löschen)
                control_freak.domain.grid[grid_x][grid_y] = EMPTY
                control_freak.domain.active_list.discard((grid_x, grid_y))
        
        control_freak.draw(rect_size)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
import pygame

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        
        # Internal list of entities to draw (for now just lines)
        self.entities = []
        
        # Grid settings
        self.show_grid = True
        self.grid_size = 50

    def world_to_screen(self, x, y):
        screen_x = int((x * self.zoom) + self.offset_x + self.width / 2)
        screen_y = int((-y * self.zoom) + self.offset_y + self.height / 2) # Y up convention
        return screen_x, screen_y

    def screen_to_world(self, sx, sy):
        wx = (sx - self.offset_x - self.width / 2) / self.zoom
        wy = -(sy - self.offset_y - self.height / 2) / self.zoom
        return wx, wy

    def pan(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy

    def adjust_zoom(self, factor, mouse_pos=None):
        # Optional: Zoom towards mouse_pos or center
        old_zoom = self.zoom
        self.zoom *= factor
        
        # Keep zoom within reasonable bounds
        self.zoom = max(0.01, min(self.zoom, 100.0))
        
        # If we wanted to zoom towards a point (like mouse), we'd adjust offsets here
        # For now, let's keep it simple: zooming towards the center of the viewport

    def draw(self, surface):
        surface.fill((30, 30, 30)) # Dark background
        
        if self.show_grid:
            self._draw_grid(surface)
            
        # Draw entities
        for entity in self.entities:
            if entity['type'] == 'line':
                p1 = self.world_to_screen(*entity['p1'])
                p2 = self.world_to_screen(*entity['p2'])
                pygame.draw.line(surface, entity['color'], p1, p2, 2)

    def _draw_grid(self, surface):
        grid_color = (60, 60, 60)
        
        # Calculate view bounds in world coordinates
        x_min, y_max = self.screen_to_world(0, 0)
        x_max, y_min = self.screen_to_world(self.width, self.height)
        
        # Dynamic grid spacing based on zoom
        effective_grid = self.grid_size
        while effective_grid * self.zoom < 20:
            effective_grid *= 2
        while effective_grid * self.zoom > 200:
            effective_grid /= 2
            
        start_x = (x_min // effective_grid) * effective_grid
        end_x = (x_max // effective_grid + 1) * effective_grid
        
        start_y = (y_min // effective_grid) * effective_grid
        end_y = (y_max // effective_grid + 1) * effective_grid
        
        curr_x = start_x
        while curr_x <= end_x:
            p1 = self.world_to_screen(curr_x, start_y)
            p2 = self.world_to_screen(curr_x, end_y)
            pygame.draw.line(surface, grid_color, p1, p2, 1)
            curr_x += effective_grid
            
        curr_y = start_y
        while curr_y <= end_y:
            p1 = self.world_to_screen(start_x, curr_y)
            p2 = self.world_to_screen(end_x, curr_y)
            pygame.draw.line(surface, grid_color, p1, p2, 1)
            curr_y += effective_grid

    def add_line(self, p1, p2, color=(200, 200, 200)):
        self.entities.append({'type': 'line', 'p1': p1, 'p2': p2, 'color': color})

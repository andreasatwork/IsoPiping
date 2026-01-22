import pygame
import math

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        
        self.show_grid = True
        self.grid_size = 100

    def world_to_screen(self, x, y, z=0):
        # Isometric projection
        # Standard iso view: X and Z axes are at 30 degrees to the horizontal
        # x_screen = (x - z) * cos(30)
        # y_screen = (x + z) * sin(30) - y
        cos30 = math.cos(math.radians(30))
        sin30 = math.sin(math.radians(30))
        
        iso_x = (x - z) * cos30
        iso_y = (x + z) * sin30 - y
        
        screen_x = int((iso_x * self.zoom) + self.offset_x + self.width / 2)
        screen_y = int((iso_y * self.zoom) + self.offset_y + self.height / 2)
        return screen_x, screen_y

    def pan(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy

    def adjust_zoom(self, factor):
        self.zoom *= factor
        self.zoom = max(0.01, min(self.zoom, 100.0))

    def draw(self, surface, system, ghost=None):
        surface.fill((30, 30, 30))
        
        if self.show_grid:
            self._draw_iso_grid(surface)
            
        # Draw system elements
        for element in system.elements:
            self._draw_element(surface, element, (200, 200, 200))

        # Draw ghost element
        if ghost:
            self._draw_element(surface, ghost, (255, 255, 0)) # Yellow for ghost

        # Draw anchor flange (red dot)
        anchor_pos = self.world_to_screen(*system.current_flange.pos.to_tuple())
        pygame.draw.circle(surface, (255, 0, 0), anchor_pos, 5)

    def _draw_element(self, surface, element, color):
        for p1, p2 in element.get_lines():
            sp1 = self.world_to_screen(*p1)
            sp2 = self.world_to_screen(*p2)
            pygame.draw.line(surface, color, sp1, sp2, 2)

    def _draw_iso_grid(self, surface):
        grid_color = (50, 50, 50)
        steps = 10
        size = self.grid_size * steps
        
        for i in range(-steps, steps + 1):
            val = i * self.grid_size
            # X lines
            p1 = self.world_to_screen(-size, 0, val)
            p2 = self.world_to_screen(size, 0, val)
            pygame.draw.line(surface, grid_color, p1, p2, 1)
            
            # Z lines
            p1 = self.world_to_screen(val, 0, -size)
            p2 = self.world_to_screen(val, 0, size)
            pygame.draw.line(surface, grid_color, p1, p2, 1)

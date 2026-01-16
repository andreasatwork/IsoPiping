import pygame
import sys
from canvas import Canvas
from input_handler import InputHandler

def main():
    pygame.init()
    
    # Configuration
    WIDTH, HEIGHT = 1200, 800
    FPS = 60
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.RESIZABLE)
    pygame.display.set_caption("IsoPiping")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Consolas", 24)
    
    canvas = Canvas(WIDTH, HEIGHT)
    input_handler = InputHandler()
    
    # Simple command processor
    def process_command(cmd):
        print(f"Executing command: {cmd}")
        parts = cmd.split()
        if not parts: return
        
        action = parts[0].lower()
        if action == "line" and len(parts) >= 5:
            try:
                x1, y1 = float(parts[1]), float(parts[2])
                x2, y2 = float(parts[3]), float(parts[4])
                canvas.add_line((x1, y1), (x2, y2))
            except ValueError:
                print("Invalid coordinates")
        elif action == "clear":
            canvas.entities = []
        elif action == "exit" or action == "quit":
            pygame.quit()
            sys.exit()

    input_handler.command_callback = process_command
    
    # Add some initial geometry for testing
    canvas.add_line((-100, 0), (100, 0), color=(255, 0, 0)) # X axis
    canvas.add_line((0, -100), (0, 100), color=(0, 255, 0)) # Y axis
    canvas.add_line((-50, -50), (50, 50), color=(0, 0, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.size
                canvas.width, canvas.height = WIDTH, HEIGHT
            
            input_handler.handle_event(event, canvas)

        # Draw
        canvas.draw(screen)
        input_handler.draw_terminal(screen, font)
        
        # Helpful info
        info_text = f"Zoom: {canvas.zoom:.2f} | Pan: ({int(canvas.offset_x)}, {int(canvas.offset_y)})"
        info_surface = font.render(info_text, True, (150, 150, 150))
        screen.blit(info_surface, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

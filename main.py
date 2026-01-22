import pygame
import sys
from canvas import Canvas
from input_handler import InputHandler
from model import PipingSystem, Vector3, Pipe, Elbow90, Flange

def main():
    pygame.init()
    
    # Configuration
    WIDTH, HEIGHT = 1200, 800
    FPS = 60
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.RESIZABLE)
    pygame.display.set_caption("IsoPiping 3D")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Consolas", 18)
    
    canvas = Canvas(WIDTH, HEIGHT)
    input_handler = InputHandler()
    system = PipingSystem()
    
    # State for insertion
    directions = [
        Vector3(1, 0, 0), Vector3(-1, 0, 0),
        Vector3(0, 1, 0), Vector3(0, -1, 0),
        Vector3(0, 0, 1), Vector3(0, 0, -1)
    ]
    dir_names = ["+X", "-X", "+Y", "-Y", "+Z", "-Z"]
    
    state = {
        'dir_idx': 0,
        'type_idx': 0, # 0: Pipe, 1: Elbow
    }

    def get_ghost():
        target_dir = directions[state['dir_idx']]
        if state['type_idx'] == 0:
            return Pipe(system.current_flange, 100)
        else:
            return Elbow90(system.current_flange, target_dir)

    running = True
    while running:
        ghost = get_ghost()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.size
                canvas.width, canvas.height = WIDTH, HEIGHT
            
            result = input_handler.handle_event(event, canvas, state)
            
            if result == "COMMIT":
                if state['type_idx'] == 0:
                    system.add_pipe(100)
                else:
                    system.add_elbow(directions[state['dir_idx']])

        # Draw
        canvas.draw(screen, system, ghost)
        input_handler.draw_terminal(screen, font)
        
        # Info overlay
        type_str = "Pipe" if state['type_idx'] == 0 else "Elbow-90"
        dir_str = dir_names[state['dir_idx']]
        info_text = f"Mode: {type_str} | Target: {dir_str} | Zoom: {canvas.zoom:.2f}"
        info_surface = font.render(info_text, True, (200, 200, 200))
        screen.blit(info_surface, (10, 10))
        
        # Shortcuts help
        help_text = "Shift+Arrows: Change Type/Dir | Enter: Insert | Arrows: Pan | +/-: Zoom"
        help_surface = font.render(help_text, True, (150, 150, 150))
        screen.blit(help_surface, (10, HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

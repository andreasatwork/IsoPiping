import pygame

class InputHandler:
    def __init__(self):
        self.terminal_mode = False
        self.current_input = ""
        self.history = []
        self.command_callback = None

    def handle_event(self, event, canvas, state):
        if event.type == pygame.KEYDOWN:
            if not self.terminal_mode:
                return self._handle_normal_keys(event, canvas, state)
            else:
                return self._handle_terminal_keys(event)
        return False

    def _handle_normal_keys(self, event, canvas, state):
        mods = pygame.key.get_mods()
        is_shift = mods & pygame.KMOD_SHIFT
        
        if is_shift:
            if event.key == pygame.K_LEFT:
                state['dir_idx'] = (state['dir_idx'] - 1) % 6
                return True
            elif event.key == pygame.K_RIGHT:
                state['dir_idx'] = (state['dir_idx'] + 1) % 6
                return True
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                state['type_idx'] = (state['type_idx'] + 1) % 2
                return True
        else:
            # Magic keys for navigation
            if event.key == pygame.K_UP:
                canvas.pan(0, 50)
            elif event.key == pygame.K_DOWN:
                canvas.pan(0, -50)
            elif event.key == pygame.K_LEFT:
                canvas.pan(50, 0)
            elif event.key == pygame.K_RIGHT:
                canvas.pan(-50, 0)
            elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                canvas.adjust_zoom(1.1)
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                canvas.adjust_zoom(0.9)
            elif event.key == pygame.K_RETURN:
                return "COMMIT"
            elif event.key == pygame.K_COLON or event.key == pygame.K_SEMICOLON: # Key to enter command mode
                self.terminal_mode = True
                self.current_input = ":"
                return True
        return False

    def _handle_terminal_keys(self, event):
        if event.key == pygame.K_RETURN:
            command = self.current_input[1:].strip()
            if command:
                self.history.append(command)
                if self.command_callback:
                    self.command_callback(command)
            self.current_input = ""
            self.terminal_mode = False
            return True
        elif event.key == pygame.K_BACKSPACE:
            if len(self.current_input) > 1: # Keep the colon
                self.current_input = self.current_input[:-1]
            else:
                self.terminal_mode = False # Exit terminal mode if backspacing past the start
                self.current_input = ""
        elif event.key == pygame.K_ESCAPE:
            self.terminal_mode = False
            self.current_input = ""
        else:
            self.current_input += event.unicode
        return True

    def draw_terminal(self, surface, font):
        if self.terminal_mode:
            # Draw a simple overlay for the terminal input
            text_surface = font.render(self.current_input, True, (255, 255, 255))
            bg_rect = text_surface.get_rect(bottomleft=(10, surface.get_height() - 10))
            bg_rect.inflate_ip(10, 10)
            pygame.draw.rect(surface, (50, 50, 50), bg_rect)
            surface.blit(text_surface, (10, surface.get_height() - bg_rect.height + 5))

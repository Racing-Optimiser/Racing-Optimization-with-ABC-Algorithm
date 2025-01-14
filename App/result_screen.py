import pygame

class Result_Screen:
    def __init__(self):
        self.running = True
        self.scroll_offset = 0  # Tracks the scroll position
        self.scroll_speed = 20  # How much to scroll per step

    def run(self, results=None):
        if results is None:
            results = ([], [])  # Default to empty lists if results are not provided
        
        screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        screen_height = screen.get_height()

        # Define button properties
        button_width, button_height = 200, 50
        button_x = (screen.get_width() - button_width) // 2
        button_y = screen_height - button_height - 20
        button_color = (50, 150, 50)
        button_hover_color = (70, 180, 70)
        button_text_color = (255, 255, 255)

        # Total height of the list
        total_content_height = max(len(results[0]) + len(results[1]), 1) * 40  # Estimate total height
        max_scroll = max(total_content_height - screen_height, 0)  # Maximum scrolling allowed

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return 'MENU'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return 'MENU'
                elif event.key == pygame.K_DOWN:  # Scroll down
                    self.scroll_offset -= self.scroll_speed
                elif event.key == pygame.K_UP:  # Scroll up
                    self.scroll_offset += self.scroll_speed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Mouse wheel up
                    self.scroll_offset += self.scroll_speed
                elif event.button == 5:  # Mouse wheel down
                    self.scroll_offset -= self.scroll_speed
                elif event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                        return 'MENU'

        # Constrain scroll_offset to avoid overscrolling
        self.scroll_offset = min(max(self.scroll_offset, -max_scroll), 0)

        # Render results[0] as a scrollable list
        y_offset = 100 + self.scroll_offset
        for index, item in enumerate(results[0]):
            text_surface = font.render(f"{index + 1}: {item}", True, (255, 255, 255))
            screen.blit(text_surface, (100, y_offset))
            y_offset += 40

        # Render results[1] as a separate list below
        y_offset += 40  # Add some padding between lists
        for index, item in enumerate(results[1]):
            text_surface = font.render(f"{index + 1}: {item}", True, (255, 255, 255))
            screen.blit(text_surface, (100, y_offset))
            y_offset += 40

        # Draw the button
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height
        pygame.draw.rect(screen, button_hover_color if is_hovered else button_color, (button_x, button_y, button_width, button_height))

        # Render button text
        button_font = pygame.font.Font(None, 36)
        button_text = button_font.render("Go to Simulation", True, button_text_color)
        text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_text, text_rect)

        # Update the display
        pygame.display.flip()

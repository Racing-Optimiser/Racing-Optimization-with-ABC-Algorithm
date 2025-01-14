import pygame

class Result_Screen:
    def __init__(self):
        self.running = True
        self.return_button = pygame.Rect(1000//2-150, 500, 300, 40) 
        # self.background_image = pygame.image.load("data/results2.jpg") 

    def run(self, results=None):
        if results is None:
            results = "No Results"
            
        screen = pygame.display.set_mode((1000, 600))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.return_button.collidepoint(event.pos):
                        screen = pygame.display.set_mode((800, 600))
                        return 'SIMULATION'

            # screen = pygame.display.get_surface()
            screen.fill((0, 0, 0))
            # screen.blit(self.background_image, (0, 0))  
            font = pygame.font.Font(None, 36)

            # Draw the button
            pygame.draw.rect(screen, '#DF0000', self.return_button, border_radius=12)
            button_text = font.render("Return to Simulation", True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=self.return_button.center)
            screen.blit(button_text, button_text_rect)
            
            # Display results
            # results_text = font.render(f"Results: {results}", True, (255, 255, 255))
            # screen.blit(results_text, (100, 250))
            y_offset = 10
            for index, item in enumerate(results[1]):
                text_surface = font.render(f"{index + 1}: {item}", True, (255, 255, 255))
                screen.blit(text_surface, (100, y_offset))
                y_offset += 40

            pygame.display.flip()

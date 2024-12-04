import pygame
import numpy as np

class Simulation:
    def __init__(self, screen, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.screen = screen
        self.width = 20
        self.height = 20
        self.margin = 5

        self.map_height = 10
        self.map_width = 10

        self.left_margin = (self.screen_width-self.map_width*(self.width+self.margin))//2
        self.top_margin = 5

        self.font = pygame.font.SysFont("Courier", 20)

        # Define fields
        self.fields = [
            Input_Field(100, self.screen_height - 150, 200, 40, self.font),
            Input_Field(350, self.screen_height - 150, 200, 40, self.font)
        ]
        self.submit_button = pygame.Rect(self.screen_width/2-100, self.screen_height - 50, 200, 40)

    def run(self, grid):
        self.screen.fill('black')
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                # Handle field events
                for field in self.fields:
                    field.handle_event(event)
                
                # Handle submit button
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.submit_button.collidepoint(event.pos):
                        print("User Input:", [field.text for field in self.fields])

            # Draw the grid
            for row in range(self.map_height):
                for col in range(self.map_width):
                    match grid[row][col]:
                        case 0:
                            color = 'white'
                        case 1:
                            color = 'blue'
                        case 2:
                            color = 'red'
                        case 3:
                            color = 'yellow'
                    pygame.draw.rect(self.screen, color, 
                                     (col * (self.width + self.margin) + self.left_margin, 
                                      row * (self.height + self.margin) + self.top_margin, 
                                      self.width, self.height))

            # Draw fields and button
            for field in self.fields:
                field.draw(self.screen)

            pygame.draw.rect(self.screen, 'green', self.submit_button)
            label = self.font.render("Run Simulation", True, (0, 0, 0))
            self.screen.blit(label, (self.submit_button.x + 10, self.submit_button.y + 10))

            pygame.display.flip()
            clock.tick(60)


class Input_Field:
    def __init__(self, x, y, width, height, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = 'white'
        self.text = ''
        self.active = False
        self.font = font

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state based on whether the mouse is over the field
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        # Change color if active
        pygame.draw.rect(screen, 'blue' if self.active else self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
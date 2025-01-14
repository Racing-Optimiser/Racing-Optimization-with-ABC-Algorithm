import pygame
import numpy as np
import json

class Simulation:
    def __init__(self, screen, screen_size):
        self.background_image = pygame.image.load("data/race_background.jpg")  
        self.screen_width, self.screen_height = screen_size
        self.screen = screen
        self.width = 20
        self.height = 20
        self.margin = 5

        self.map_height = 10
        self.map_width = 10

        self.left_margin = (self.screen_width - self.map_width * (self.width + self.margin)) // 2
        self.top_margin = 5

        self.font = pygame.font.SysFont("Courier", 20)

        self.fields = [
            Input_Field(20, self.screen_height - 250, 200, 40, self.font, "Race Index"),
            Input_Field(20, self.screen_height - 150, 200, 40, self.font, "Max. Iteracji"),
            Input_Field(self.screen_width / 3 + 20, self.screen_height - 150, 200, 40, self.font, "Ilość pszczół"),
            Input_Field(2 * self.screen_width / 3 + 20, self.screen_height - 150, 200, 40, self.font, "Limit pożywienia"),
        ]

        self.submit_button = pygame.Rect((self.screen_width / 2) - 100, self.screen_height - 50, 200, 40)

        self.race_idx_description = pygame.Rect(300, self.screen_height - 300, 400, 100)
        self.current_description = ""  

    def run(self, grid):
        self.screen.blit(self.background_image, (0, 0))  

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                for field in self.fields:
                    field.handle_event(event)
                
                race_idx_field = self.fields[0] 
                if race_idx_field.text != race_idx_field.previous_value and race_idx_field.text != '':
                    # print(f"Race Index changed from {race_idx_field.previous_value} to {race_idx_field.text}")
                    race_idx_field.previous_value = race_idx_field.text
                    
                    race_list = ['data/race_simulation.json','data/race_simulation1.json','data/race_simulation2.json']
                    idx = int(race_idx_field.previous_value)
                    if idx<4 and idx>0:
                        with open(race_list[idx-1], "r") as file:
                            race_data = json.load(file) 
                        self.current_description = f"Race Description: Index {race_idx_field.text}"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.submit_button.collidepoint(event.pos):
                        parameters = [field.text for field in self.fields]
                        if not '' in parameters:
                            print("User Input:", parameters)
                            return 'RACING', [int(parameters[1]), int(parameters[2]), int(parameters[3])], int(parameters[0])

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

            # Draw input fields and labels
            for field in self.fields:
                field.draw(self.screen)

            # Draw the race description text
            pygame.draw.rect(self.screen, 'black', self.race_idx_description, border_radius=5)
            if self.current_description:
                race_description = self.font.render(self.current_description, True, 'white')
                self.screen.blit(race_description, (self.race_idx_description.x + 10, self.race_idx_description.y + 10))

            pygame.draw.rect(self.screen, '#DF0000', self.submit_button, border_radius=12)
            label = self.font.render("Run Simulation", True, (0, 0, 0))
            self.screen.blit(label, (self.submit_button.x + 10, self.submit_button.y + 10))

            pygame.display.flip()
            clock.tick(60)


class Input_Field:
    def __init__(self, x, y, width, height, font, label_text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = 'white'
        self.text = ''
        self.active = False
        self.font = font
        self.label_text = label_text
        self.label_surface = font.render(label_text, True, 'white')
        self.previous_value = ''  


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        label_background = pygame.Rect(self.rect.x - 5, self.rect.y - 35, self.label_surface.get_width() + 10, self.label_surface.get_height() + 10)
        pygame.draw.rect(screen, 'black', label_background, border_radius=5)
        screen.blit(self.label_surface, (self.rect.x, self.rect.y - 30))
        
        pygame.draw.rect(screen, '#329fda' if self.active else self.color, self.rect, border_radius=12)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

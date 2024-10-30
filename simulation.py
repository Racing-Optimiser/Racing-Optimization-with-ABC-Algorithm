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

        self.active_button = None
        
        self.bot_position = [0, 0]
        self.exit_position = [9, 9]
        self.font = pygame.font.SysFont("Courier", 20)
        
        buttons_margin = 20
        interval = (self.screen_width-2*buttons_margin)//4
        buttons_height = (self.map_height + self.margin)*self.height + buttons_margin
        self.buttons = {
            'Right-hand': pygame.Rect(buttons_margin,   buttons_height, interval-50, 50),
            'A*'        : pygame.Rect(interval*1,       buttons_height, interval-buttons_margin, 50),
            'Dijkstra'  : pygame.Rect(interval*2,       buttons_height, interval-buttons_margin, 50),
            'Floodfill' : pygame.Rect(interval*3,       buttons_height, interval-buttons_margin, 50),
            'Return to menu': pygame.Rect(buttons_margin,   10, interval-buttons_margin+50, 50),
            'Launch simulation': pygame.Rect(self.screen_width/3,  buttons_height+100, self.screen_width/3, 50),
        }


    def run(self, grid):
        self.screen.fill('black')
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()
                    for text, rect in self.buttons.items():
                        if rect.collidepoint(mouse):
                            if text == 'Right-hand':
                                self.active_button = text
                            elif text == 'A*':
                                self.active_button = text
                            elif text == 'Dijkstra':
                                self.active_button = text
                            elif text == 'Floodfill':
                                self.active_button = text
                            elif text == 'Return to menu':
                                return "MENU"
                            elif text == 'Launch simulation':
                                self.active_button = text

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
                    pygame.draw.rect(self.screen, color, (col * (self.width + self.margin) + self.left_margin, row * (self.height + self.margin) + self.top_margin, self.width, self.height))
    
            for text, rect in self.buttons.items():
                if self.active_button == text:
                    pygame.draw.rect(self.screen, 'Green', rect)
                else:
                    pygame.draw.rect(self.screen, 'white', rect)
                label = self.font.render(text, True, (0, 0, 0))
                self.screen.blit(label, (rect.x + 20, rect.y + 10))
            pygame.display.flip()
            clock.tick(60)

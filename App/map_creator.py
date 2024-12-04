import pygame
import numpy as np

class MapCreator:
    def __init__(self, screen, screen_size, grid=np.full((10, 10), 0)):
        self.background_image = pygame.image.load("data/track_background.jpg")  
        self.screen_width, self.screen_height = screen_size
        self.screen = screen
        self.grid = grid
        self.width = 20
        self.height = 20
        self.margin = 5

        self.map_height = 10
        self.map_width = 10

        self.left_margin = (self.screen_width-self.map_width*(self.width+self.margin))//2
        self.top_margin = 5

        self.place_bot = False
        self.place_exit = False
        self.make_walls = False

        self.active_button = None
        
        self.bot_position = [0, 0]
        self.exit_position = [9, 9]
        self.font = pygame.font.SysFont(None, 24)
        
        buttons_margin = 20
        interval = (self.screen_width-2*buttons_margin)//4
        buttons_height = (self.map_height + self.margin)*self.height + buttons_margin
        self.buttons = {
            'Place track': pygame.Rect(buttons_margin, buttons_height, interval-50, 50),
            'Place Start': pygame.Rect(interval*1, buttons_height, interval-buttons_margin, 50),
            'Place Exit': pygame.Rect(interval*2, buttons_height, interval-buttons_margin, 50),
            'Finished': pygame.Rect(interval*3, buttons_height, interval-buttons_margin, 50)
        }
    def run(self):
        self.screen.blit(self.background_image, (0, 0))  
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
                            print("collision")
                            if text == 'Place track':
                                self.make_walls = True
                                self.place_exit = False
                                self.place_bot = False
                                self.active_button = text
                            elif text == 'Place Start':
                                self.place_bot = True
                                self.make_walls = False
                                self.place_exit = False
                                self.active_button = text
                            elif text == 'Place Exit':
                                self.place_exit = True
                                self.place_bot = False
                                self.make_walls = False
                                self.active_button = text
                            elif text == 'Finished':
                                return 'MENU', self.grid

                    mouse = ((mouse[0] - self.left_margin) // (self.width + self.margin), (mouse[1] - self.top_margin) // (self.height + self.margin))
                    if 0 <= mouse[0] < 10 and 0 <= mouse[1] < 10:
                        if self.make_walls:
                                self.grid[mouse[1], mouse[0]] = 1 if self.grid[mouse[1], mouse[0]] == 0 else 0
                        elif self.place_bot:
                                #cleanup
                                self.grid[self.bot_position[0], self.bot_position[1]] = 0
                                self.bot_position = [mouse[1], mouse[0]]
                                self.grid[mouse[1], mouse[0]] = 2

                        elif self.place_exit:
                                #cleanup
                                self.grid[self.exit_position[0], self.exit_position[1]] = 0
                                self.exit_position = [mouse[1], mouse[0]]
                                self.grid[mouse[1], mouse[0]] = 3

            for row in range(self.map_height):
                for col in range(self.map_width):
                    match self.grid[row][col]:
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


if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600)) 
    mapcreator = MapCreator(screen, (800, 600))
    mapcreator.run()
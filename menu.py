import pygame
import sys

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Courier", 50)
        self.title_font = pygame.font.SysFont("Papyrus", 80)  # Larger font for the title
        self.background_image = pygame.image.load("background.jpg")  
        self.buttons = {
            'Map Creator': pygame.Rect(150, 200, 500, 50),
            'Run Simulation': pygame.Rect(150, 300, 500, 50),
            'Quit': pygame.Rect(150, 400, 500, 50)
        }

    def draw_title(self):
        title_text = self.title_font.render("Racing menager", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)

    def draw_buttons(self, mouse_pos):
        for text, rect in self.buttons.items():
            #hover effect
            color = 'grey' if rect.collidepoint(mouse_pos) else 'white'
            pygame.draw.rect(self.screen, color, rect, border_radius=12) 

            label = self.font.render(text, True, (0, 0, 0))
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.blit(self.background_image, (0, 0))  
            self.draw_title()  

            mouse_pos = pygame.mouse.get_pos()
            self.draw_buttons(mouse_pos)  

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for text, rect in self.buttons.items():
                        if rect.collidepoint(mouse_pos):
                            if text == 'Map Creator':
                                return 'MAP_CREATOR'
                            elif text == 'Run Simulation':
                                return 'SIMULATION'
                            elif text == 'Quit':
                                pygame.quit()
                                sys.exit()

            pygame.display.flip()
            clock.tick(60)

pygame.init()
screen = pygame.display.set_mode((800, 600))

menu = Menu(screen)
menu.run()

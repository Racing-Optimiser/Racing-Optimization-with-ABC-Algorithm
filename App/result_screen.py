import pygame
class Result_Screen:
    def __init__(self):
        self.running = True 

    def run(self, results = None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return 'MENU' 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    self.running = False
                    return 'MENU'

        screen = pygame.display.get_surface()
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Wyniki: {results}", True, (255, 255, 255))
        screen.blit(text, (100, 250)) 

        pygame.display.flip()  
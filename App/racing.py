import pygame
from ABC_algorithm2 import abc_algorithm_demo
import threading
import math

def draw_spinner(screen, angle, center, radius):
    end_x = center[0] + radius * math.cos(angle)
    end_y = center[1] + radius * math.sin(angle)
    pygame.draw.line(screen, (255, 255, 255), center, (end_x, end_y), 3)

class Racing:
    def __init__(self, screen, screen_size):
        self.background_image = pygame.image.load("data/clock.jpeg") 
        self.background_image = pygame.transform.scale(self.background_image, (screen_size[0], screen_size[1]))

        self.screen = screen 
        self.running = True
        self.algorithm_thread = None
        self.algorithm_done = False
        self.angle = 0  
        self.result = None


    def run_algorithm(self, parameters):
        best_solutions, best_strategies = abc_algorithm_demo(parameters[0], parameters[1], parameters[2])
        self.algorithm_done = True
        self.result = best_solutions, best_strategies

    def run(self, parameters):
        if self.algorithm_thread is None:
            self.algorithm_thread = threading.Thread(target=self.run_algorithm, args=(parameters,))
            self.algorithm_thread.start()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return 'MENU', None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return 'MENU', None

        screen = pygame.display.get_surface()
        screen.blit(self.background_image, (0, 0))  

        center = (screen.get_width() // 2, screen.get_height() // 2)

        if not self.algorithm_done:
            self.angle += 0.1
            draw_spinner(screen, self.angle, center, 50)
        else:
            return 'RESULT_SCREEN', self.result

        
 
        pygame.display.flip()
        pygame.time.delay(100)

        # return None if not self.algorithm_done else 'RESULT_SCREEN', self.result

import pygame

class Result_Screen:
    def __init__(self):
        self.running = True
        self.return_button = pygame.Rect(1300 - 300, 700, 300, 40)
        self.time_field = pygame.Rect((1300 * 2) // 3 - 300, 700, 300, 40)
        self.memory_field = pygame.Rect(1300 // 3 - 300, 700, 300, 40)
        # self.background_image = pygame.image.load("data/results2.jpg")

    def run(self, results=None):
        if results is None:
            results = "No Results"

        screen = pygame.display.set_mode((1300, 800))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.return_button.collidepoint(event.pos):
                        screen = pygame.display.set_mode((800, 600))
                        return 'SIMULATION'

            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 36)

            pygame.draw.rect(screen, '#DF0000', self.return_button, border_radius=12)
            button_text = font.render("Symulacja", True, (255, 255, 255))
            button_text_rect = button_text.get_rect(center=self.return_button.center)
            screen.blit(button_text, button_text_rect)

            pygame.draw.rect(screen, 'blue', self.time_field, border_radius=12)
            time_text = font.render(f"Czas:{round(results[3], 3)} s", True, (255, 255, 255))
            time_text_rect = time_text.get_rect(center=self.time_field.center)
            screen.blit(time_text, time_text_rect)

            pygame.draw.rect(screen, 'blue', self.memory_field, border_radius=12)
            memory_text = font.render(f"Pamięć:{round(results[3], 3)} KB", True, (255, 255, 255))
            memory_text_rect = memory_text.get_rect(center=self.memory_field.center)
            screen.blit(memory_text, memory_text_rect)

            best_solution_index, best_solution_value = min(enumerate(results[0]), key=lambda x: x[1])
            best_strategy = results[1][best_solution_index]

            best_solution_text = font.render(f"Najlepsze rozwiązanie: {best_solution_value} s", True, (255, 255, 255))
            best_strategy_text = font.render(f"Najlepsza strategia: {best_strategy}", True, (255, 255, 255))
            hamulce = font.render(f"Max. poziom zużycia hamulców: {best_strategy[0]}", True, (255, 255, 255))
            silnik = font.render(f"Max. poziom zużycia silnika: {best_strategy[1]}", True, (255, 255, 255))
            zawieszenie = font.render(f"Max. poziom zużycia zawieszenia: {best_strategy[2]}", True, (255, 255, 255))
            opony = font.render(f"Kolejność używania opon: {best_strategy[3]}", True, (255, 255, 255))
            paliwo = font.render(f"Minimalny poziom paliwa: {best_strategy[4]}", True, (255, 255, 255))
            zuzycie_opon = font.render(f"Max. poziom zużycia opon: {best_strategy[5]}", True, (255, 255, 255))
            moc = font.render(f"Limit mocy pojazdu: {best_strategy[6]}", True, (255, 255, 255))
            screen.blit(best_solution_text, (100, 100))
            screen.blit(best_strategy_text, (100, 180))
            screen.blit(hamulce, (100, 220))
            screen.blit(silnik, (100, 260))
            screen.blit(zawieszenie, (100, 300))
            screen.blit(opony, (100, 340))
            screen.blit(paliwo, (100, 380))
            screen.blit(zuzycie_opon, (100, 420))
            screen.blit(moc, (100, 460))

            pygame.display.flip()

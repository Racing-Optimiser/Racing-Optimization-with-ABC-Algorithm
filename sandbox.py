import pygame
import numpy as np

pygame.init()
screen_width, screen_height = 255, 300  # Increased height for the button
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
width = 20
height = 20
margin = 5
empty_color = 'white'
wall_color = 'blue'
button_color = 'grey'
button_text_color = 'black'
button_rect = pygame.Rect(75, 260, 100, 30)  # Button dimensions
button_text = 'Make Walls'
font = pygame.font.SysFont(None, 24)

# Grid array for the map
grid = np.full((10, 10), 0)
make_walls = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse):
                make_walls = not make_walls
                button_text = 'Make Walls' if not make_walls else 'Stop Making Walls'
            else:
                mouse = (mouse[0] // (width + margin), mouse[1] // (height + margin))
                if 0 <= mouse[0] < 10 and 0 <= mouse[1] < 10:
                    grid[mouse[1], mouse[0]] = 1 if make_walls else 0

    # Fill screen with white color
    screen.fill((255, 255, 255))

    # Draw the grid
    for row in range(10):
        for col in range(10):
            color = wall_color if grid[row][col] == 1 else empty_color
            pygame.draw.rect(screen, color, (col * (width + margin) + margin, row * (height + margin) + margin, width, height))

    # Draw the button
    pygame.draw.rect(screen, button_color, button_rect)
    text = font.render(button_text, True, button_text_color)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()

import pygame
import numpy as np

pygame.init()
scr_width = 500
scr_height = 350
screen = pygame.display.set_mode((scr_width, scr_height))
clock = pygame.time.Clock()
running = True
width = 20
height = 20
margin = 5
top_margin = 5
left_margin = (scr_width-10*(width+margin))//2
empty_color = 'white'
wall_color = 'blue'

button_color = 'grey'
button_text_color = 'black'
button_rect = pygame.Rect(75, 260, 100, 30)  
font = pygame.font.SysFont(None, 24)

button1 = "Create walls"
button2 = "Place the robot"
button3 = "Place exit"
button4 = "Finish labirynth"


# a array we can work on for coding
grid = np.full((10, 10), 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            mouse = pygame.mouse.get_pos()
            mouse = ((mouse[0] - left_margin ) // (width + margin), (mouse[1] - top_margin) // (height + margin))
            # print(mouse)
            if 0 <= mouse[0] < 10 and 0 <= mouse[1] < 10: 
                grid[mouse[1], mouse[0]] = 1 if grid[mouse[1], mouse[0]] == 0 else 0

    # creating an empty map
    for row in range(10):
        for col in range(10):
            if grid[row][col] == 1:
                color = wall_color
            else:
                color = empty_color
            pygame.draw.rect(screen, color, (col*(width + margin)+left_margin, row*(height + margin) + top_margin, width, height))
   
    # creating buttons
    pygame.draw.rect(screen, button_color, button_rect)
    text = font.render(button1, True, button_text_color)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
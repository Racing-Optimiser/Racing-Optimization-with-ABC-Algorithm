import pygame
from menu import Menu
from map_creator import MapCreator
from simulation import Simulation
import numpy as np

pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size) 
clock = pygame.time.Clock()

MENU, MAP_CREATOR, SIMULATION = 'MENU', 'MAP_CREATOR', 'SIMULATION'

# Initial game state
current_state = MENU
grid=np.full((10, 10), 0)
menu = Menu(screen)
map_creator = MapCreator(screen, screen_size)
simulation = Simulation(screen, screen_size)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # State management
    if current_state == MENU:
        next_state = menu.run()
        if next_state:
            current_state = next_state
    elif current_state == MAP_CREATOR:
        next_state, grid = map_creator.run()
        if next_state:
            current_state = next_state
    elif current_state == SIMULATION:
        next_state = simulation.run(grid)
        if next_state:
            current_state = next_state
        # else:
        #     print("nie stworzyłeś mapy!")
        #     current_state = MENU
           

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

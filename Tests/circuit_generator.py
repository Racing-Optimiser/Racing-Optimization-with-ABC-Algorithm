import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import numpy as np

points = []

def onclick(event):
    if event.inaxes: 
        x, y = event.xdata, event.ydata
        points.append((x, y))
        ax.plot(x, y, 'ro')  
        fig.canvas.draw()  
        #ilość punktów które klika użytkownik
        if len(points) == 10:
            print(complete_circuit())


# łączę punkt z najbliższym sąsiadem, zaczynając od pierwszego
def complete_circuit():
    if len(points) > 1:
        remaining_points = points.copy()  
        connected_order = [remaining_points.pop(0)]  
        distance = 0
        angle = 0
        while remaining_points:
            current_point = connected_order[-1]
            distances = cdist([current_point], remaining_points) 
            nearest_idx = np.argmin(distances) 
            nearest_point = remaining_points.pop(nearest_idx) 
            distance += np.sqrt((current_point[0]-nearest_point[0])**2 + (current_point[1]-nearest_point[1])**2)
            connected_order.append(nearest_point)
            ax.plot([current_point[0], nearest_point[0]], [current_point[1], nearest_point[1]], 'b-')
            fig.canvas.draw()
        #połącz ostatni punkt z pierwszym
        distance += np.sqrt((connected_order[-1][0]-connected_order[0][0])**2 + (connected_order[-1][1]-connected_order[0][1])**2)

        ax.plot(
            [connected_order[-1][0], connected_order[0][0]],
            [connected_order[-1][1], connected_order[0][1]],
            'b-'
        )
        fig.canvas.draw()
    return distance, angle

fig, ax = plt.subplots()
ax.set_xlim(0, 5)
ax.set_ylim(0, 5)
ax.set_title("Wyklikaj zaryus kształtu toru")
ax.grid(True)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

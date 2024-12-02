import numpy as np
import matplotlib.pyplot as plt

 # Funkcja celu
def objective(food_source):
    x = food_source[0]
    y = food_source[1]
    # return x**2 + y**2  # Funkcja f(x, y) = x^2 + y^2
    return x * np.exp(-x**2-y**2)

def abc_algorithm_demo():
    # Parametry algorytmu
    dim = 3  # Liczba wymiarów, u nas przeba będzie dobrać tyle ile będzie zmiennych
    num_bees = 20  # Liczba pszczół
    max_iter = 100  # Maksymalna liczba iteracji
    food_limit = 50  # Limit wyczerpania źródła pożywienia
    lb, ub = -10, 10  # Dolne i górne ograniczenie

    
    # Inicjalizacja
    #losowe wartości x i y w danym przedziale
    food_sources = (lb + (ub - lb) * np.random.rand(num_bees, dim))
        
    fitness = []
    for food in food_sources:
        fitness.append(objective(food))
    trial_counter = np.zeros(num_bees)

    best_fitness = np.min(fitness)
    best_solutions = [best_fitness]

    # Główna pętla algorytmu
    for _ in range(max_iter):
        # Faza pszczół robotnic
        for i in range(num_bees):
            partner = np.random.randint(num_bees)
            phi = np.random.uniform(-1, 1, dim)# phi jest odpowiedzialne za eksplorację bo wyznacza kolejnego kandydata, powinno być losowe
            candidate = food_sources[i] + phi * (food_sources[i] - food_sources[partner])
            candidate = np.clip(candidate, lb, ub) # np.minimum(a_max, np.maximum(a, a_min))
            candidate_fitness = objective(candidate)
            
            #sprawdzam, czy kandydat jest lepszy od obecnego
            if candidate_fitness < fitness[i]:
                food_sources[i] = candidate
                fitness[i] = candidate_fitness
                #zeruję jego ilość jedzenia
                trial_counter[i] = 0
            else:
                #jeśli ponownie "zwyciężyło" aktualne, to dodaję licznik (to on zapobiega stagnacji)
                trial_counter[i] += 1

        # Faza pszczół obserwatorów
        #im większa jakość źródła tym większe prawdopodobieństwo jego wyboru,
        #ale słabe źródła też mogą być wybrane co uchrania przed utknięciem w minimum lokalnym
        prob = fitness / np.sum(fitness)
        for i in range(num_bees):
            selected = roulette_wheel_selection(prob)
            partner = np.random.randint(num_bees)
            phi = np.random.uniform(-1, 1, dim)
            candidate = food_sources[selected] + phi * (food_sources[selected] - food_sources[partner])
            candidate = np.clip(candidate, lb, ub)
            candidate_fitness = objective(candidate)

            if candidate_fitness < fitness[selected]:
                food_sources[selected] = candidate
                fitness[selected] = candidate_fitness
                trial_counter[selected] = 0
            else:
                trial_counter[selected] += 1

        # Faza pszczół zwiadowców, sprawdzamy czy wyczerpaliśmy ilość źródeł jedzenia
        #i szukamy losowo nowych
        for i in range(num_bees):
            if trial_counter[i] > food_limit:
                food_sources[i] = lb + (ub - lb) * np.random.rand(dim)
                fitness[i] = objective(food_sources[i])
                trial_counter[i] = 0

        # Zapis najlepszych wyników
        current_best = np.min(fitness)
        if current_best < best_fitness:
            best_fitness = current_best
        best_solutions.append(best_fitness)

    # Wizualizacja wyników
    visualize_optimization(food_sources, objective, lb, ub, best_solutions)

#selekcja probabilistyczna (ruletka)
def roulette_wheel_selection(prob):
    cumulative = np.cumsum(prob)
    r = np.random.rand()
    return np.searchsorted(cumulative, r)

def visualize_optimization(food_sources, objective, lb, ub, best_solutions):
    # Rysowanie powierzchni funkcji
    x = np.linspace(lb, ub, 100)
    y = np.linspace(lb, ub, 100)
    X, Y = np.meshgrid(x, y)
    Z = objective(np.array([X, Y]))

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Powierzchnia funkcji z pozycjami pszczół
    ax = axes[0]
    ax.contourf(X, Y, Z, levels=50, cmap='viridis')
    ax.scatter(food_sources[:, 0], food_sources[:, 1], c='red', s=50, label='Pszczoły')
    ax.set_title('Pozycje pszczół na funkcji celu')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()

    # Postęp optymalizacji
    ax = axes[1]
    ax.plot(best_solutions, label='Najlepsze rozwiązanie', color='blue')
    ax.set_title('Postęp optymalizacji')
    ax.set_xlabel('Iteracje')
    ax.set_ylabel('Najlepsze f(x, y)')
    ax.grid(True)
    ax.legend()

    plt.tight_layout()
    plt.show()

# Uruchomienie algorytmu
abc_algorithm_demo()

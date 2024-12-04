import numpy as np
import matplotlib.pyplot as plt
import random
import json
from car_failure import CarFailure
from race_car import RaceCar
from weather_class import Weather
from tires_class import Tire
 # Funkcja celu
failure_list = './data/failure_list.json'
weather_list = 'data/weather_conditions.json'
tire_list = 'data/tires_characteristics.json'

car = RaceCar(
        make="Toyota",
        model="GR010 Hybrid",
        top_speed=340,
        horsepower=680,
        weight=1040,
        fuel_tank_capacity=35,
        average_fuel_consumption=2,
        lap_time=210
        )
with open("data/race_simulation.json", "r") as file:
    race_data = json.load(file)

def calculate_total_time(race_data, strategy):
    total_time = 0
    pitstop_intervals = strategy[0]
    tires = strategy[1]
    fuel_pitstop = strategy[2]
    tire_wear_str = strategy[3]
    lap1 = race_data[0]
    tire_wear = lap1["lap_data"]["tire_wear"]
    fuel_level = lap1["lap_data"]["fuel_level"]
    lap_time_start = lap1["lap_data"]["lap_time"]
    
    
    for lap in race_data:
        
        
        failure = lap["lap_data"]["failure"]
        weather = lap["lap_data"]["weather"]
        failures_list = []
        #pobreanie obiektu z nazwy 

        failure = get_failure_by_name(failure,CarFailure.load_from_file(failure_list))
        failures_list.append(failure)
        



        lap_number = lap['lap_number']

        lap_time = lap_time_with_actuall_conditions(failures_list,lap_time_start,tires,tire_wear,weather)
        # Adjust lap time for tire wear and weather conditions
        
        adjusted_lap_time = lap_time + (tire_wear * 10)  # Increase time for tire wear
        
        
        # Check if a pitstop is required (e.g. fuel or tire change)
        if fuel_level < fuel_pitstop or tire_wear < tire_wear_str :
            tires,tires_wear,actuall_failures, pitstop_time,fuel_level,pitstop_data = pitstop(car, tires,fuel_level, failures_list,repair = True,tire_change = True,fuel = True)
        elif lap_number == pitstop_intervals:
            tires,tires_wear,actuall_failures, pitstop_time,fuel_level,pitstop_data = pitstop(car, tires,fuel_level, failures_list,repair = True,tire_change = True,fuel = True)
        else:
            pitstop_time = 0
        
       
        total_time += lap_time + pitstop_time
    
    #fajnie by było tu wyświetlać która to była kalkulacja
    print("Calculation nr: ")
    return total_time

def get_tire_by_name(name, tires):
    for tire in tires:
        if tire.name.lower() == name.lower():  # Ignoruje wielkość liter
            return tire
    return None  # Jeśli nie znaleziono opony

def get_failure_by_name(name,failure_list):
    for failure in failure_list:
        if  failure.name.lower() == name.lower():  # Ignoruje wielkość liter
            return failure
    return None

def get_weather_by_name(name,weather_list):
    for weather in weather_list:
        if  weather.name.lower() == name.lower():  # Ignoruje wielkość liter
            return weather
    return None  



def abc_algorithm_demo():
    # Parametry algorytmu
    dim = 4  # Liczba wymiarów
    num_bees = 10  # Liczba pszczół
    max_iter = 50  # Maksymalna liczba iteracji
    food_limit = 50  # Limit wyczerpania źródła pożywienia
    bounds = [
        (1, 20),  # Interwały pitstopow
        ['soft', 'medium', 'hard', 'wet'],  # Strategia opon
        (1, 35),  # Strategia paliwa
        (0.1, 1)  # Zużycie opon
    ]

    # Inicjalizacja
    population = [
        [
            random.randint(*bounds[0]),  # Interwały pitstopow
            random.choice(bounds[1]),  # Strategia opon
            random.randint(*bounds[2]),  # Strategia paliwa
            random.uniform(*bounds[3])  # Strategia zużycia opon
        ]
        for _ in range(num_bees)
    ]

    fitness = [calculate_total_time(race_data, strategy) for strategy in population]
    trial_counter = np.zeros(num_bees)

    best_fitness = min(fitness)
    best_solutions = [best_fitness]

    # Główna pętla algorytmu
    for _ in range(max_iter):
        # Faza pszczół robotnic
        for i in range(num_bees):
            partner = random.randint(0, num_bees - 1)
            phi = np.random.uniform(-1, 1)
            candidate = []
            for j in range(dim):
                if j == 1:  # Strategia opon (string)
                    candidate.append(random.choice(bounds[1]))
                else:
                    candidate_value = population[i][j] + phi * (population[i][j] - population[partner][j])
                    candidate_value = max(bounds[j][0], min(candidate_value, bounds[j][1]))  # Klipowanie
                    candidate.append(candidate_value)
            candidate_fitness = calculate_total_time(race_data, candidate)

            if candidate_fitness < fitness[i]:
                population[i] = candidate
                fitness[i] = candidate_fitness
                trial_counter[i] = 0
            else:
                trial_counter[i] += 1

        # Faza pszczół obserwatorów
        prob = fitness / np.sum(fitness)
        for i in range(num_bees):
            selected = roulette_wheel_selection(prob)
            partner = random.randint(0, num_bees - 1)
            phi = np.random.uniform(-1, 1)
            candidate = []
            for j in range(dim):
                if j == 1:  # Strategia opon (string)
                    candidate.append(random.choice(bounds[1]))
                else:
                    candidate_value = population[selected][j] + phi * (population[selected][j] - population[partner][j])
                    candidate_value = max(bounds[j][0], min(candidate_value, bounds[j][1]))
                    candidate.append(candidate_value)
            candidate_fitness = calculate_total_time(race_data, candidate)

            if candidate_fitness < fitness[selected]:
                population[selected] = candidate
                fitness[selected] = candidate_fitness
                trial_counter[selected] = 0
            else:
                trial_counter[selected] += 1

        # Faza pszczół zwiadowców
        for i in range(num_bees):
            if trial_counter[i] > food_limit:
                population[i] = [
                    random.randint(*bounds[0]),
                    random.choice(bounds[1]),
                    random.randint(*bounds[2]),
                    random.uniform(*bounds[3])
                ]
                fitness[i] = calculate_total_time(race_data, population[i])
                trial_counter[i] = 0

        # Zapis najlepszych wyników
        current_best = min(fitness)
        if current_best < best_fitness:
            best_fitness = current_best
        best_solutions.append(best_fitness)

    # Wizualizacja wyników (opcjonalnie)
    # visualize_optimization(population, calculate_total_time, lb, ub, best_solutions)
    print(best_solutions)
    return best_solutions


def pitstop(car, tires,fuel_level, actuall_failures,repair = True,tire_change = True,fuel = True):
    """
    Funkcja symulująca pitstop: wymiana opon, naprawa usterek, uzupełnienie paliwa.
    """
    total_repair_time = 0
    total_pit_time = 0
    if tire_change:
    # Wymiana opon na nowe (przywracamy pełną wydajność)
        
        tires_list = Tire.load_from_file(tire_list)
        
        new_tire = get_tire_by_name(tires,tires_list)
        tires = new_tire

        tires_wear = 1
        tires_change_time = 20
    
    # Uzupełnienie paliwa
    if fuel:
        refuel = car.fuel_tank_capacity - fuel_level  # Maksymalna pojemność baku
        time_refuel = 10 + refuel * 2
        fuel_level = car.fuel_tank_capacity
    
    failure_names = []
    if repair and actuall_failures[0]:
    # Naprawa usterek
       
        for failure in actuall_failures:

            failure_names.append(failure.name)
            total_repair_time += failure.fixtime  # Sumujemy czas naprawy
      # Sumujemy utratę wydajności
    
    # Można zresetować awarie po naprawach
    actuall_failures.clear()


    # Pitstop trwa również określony czas
    pitstop_time = 30 + total_repair_time + time_refuel + tires_change_time  # Zliczamy czas pitstopu i naprawy
    
    pitstop_data = {
        "repairs" : failure_names,
        "fuel_amount" : refuel,
        "tires_change" : tire_change,
        "time in pitstop" : pitstop_time

    }
    # Zwracamy nowe opony, czas pitstopu oraz naprawy
    return tires.name,tires_wear,actuall_failures, pitstop_time,fuel_level,pitstop_data

def lap_time_with_actuall_conditions(actuall_failures,lap_time,tires,tires_wear,weather):
    try:

        reductions = [failure.speed_reduction for failure in actuall_failures]
    except:
        reductions = None
    max_red = 0
    if reductions:
        max_red = max(reductions)

    weather = get_weather_by_name(weather,Weather.load_from_file(weather_list))
    wet_level = weather.wet
    tires = get_tire_by_name(tires,Tire.load_from_file(tire_list))

    tires_wet_cap = tires.wet_performance
    wet_reduction = 0
    #procentowe obnizenie predkosci okrazenia w zwiazku z mokroscia jezdzni oraz przyczepnosci
    if wet_level > 0:
        wet_reduction = wet_level - tires_wet_cap
        if wet_reduction < 0:
            wet_reduction = 0

    
    grip_tires = tires.grip
    grip_weather = weather.surface_grip

    grip_red = grip_weather - grip_tires
    if grip_red < 0:
        grip_red = 0

    

    return lap_time + lap_time * max_red + lap_time * wet_reduction + lap_time * grip_red + lap_time * (1 - tires_wear)



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


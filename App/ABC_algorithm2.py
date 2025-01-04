import numpy as np
import matplotlib.pyplot as plt
import random
import json
import psutil
import os
import time
from car_failure import CarFailure
from race_car import RaceCar
from weather_class import Weather
from tires_class import Tire
from brakes_failure_class import BrakesFailure
from engine_failure_class import EngineFailure
from suspension_failure_class import SuspensionFailure
from tires_failure_class import TiresFailure

#pobranie możliwych usterek dla danego podzespołu i w jakim momencie zużycia jest ryzyko ich wystąpienia
failures_engine = EngineFailure.load_from_file()
thresholds_engine = [[failure.name, failure.engine_threshold ] for failure in failures_engine]

failures_brakes = BrakesFailure.load_from_file()
thresholds_brakes = [[failure.name, failure.brake_threshold ] for failure in failures_brakes]

failures_suspension = SuspensionFailure.load_from_file()
thresholds_suspension = [[failure.name, failure.suspension_threshold ] for failure in failures_suspension]

failures_tires = TiresFailure.load_from_file()
thresholds_tires = [[failure.name, failure.tires_threshold ] for failure in failures_tires]

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
        average_fuel_consumption=3, #power*avg_fuel_consumption
        lap_time=210
        )
with open("data/race_simulation.json", "r") as file:
    race_data = json.load(file)
 
 # Funkcja celu
def calculate_total_time(race_data, strategy):
    total_time = 0
    #pobranie strategii
    brakes_wear_strat = strategy[0]
    engine_wear_strat = strategy[1]
    suspension_wear_strat = strategy[2]
    tires = strategy[3]
    fuel_pitstop = strategy[4]
    tire_wear_str = strategy[5]
    car_power = strategy[6]
    #Pobranie danych o 1 okrążeniu
    lap1 = race_data[0] 
    tire_wear = lap1["lap_data"]["tire_wear"]
    fuel_level = lap1["lap_data"]["fuel_level"]
    lap_time_start = lap1["lap_data"]["lap_time"] 
    failures_list = []

    parts_wear = {
        "Engine" : 1,
        "Suspension" : 1,
        "Brakes" : 1,
    }

    parts_degrad = {
        "Engine": 0.02,
        "Suspension": 0.01,
        "Brakes": 0.04,
    }   

    #zmiana zużycia części w zależności od mocy auta
    parts_degrad = {part: parts_degrad[part] + (parts_degrad[part] * car_power) for part in parts_degrad}
    tires_degrad = get_tire_by_name(tires,Tire.load_from_file(tire_list))
    tires_degrad = tires_degrad.degradation_rate
    #zmiana podstawowego czasu okrążenia gdy ograniczamy moc


    lap_time_start = lap_time_start + lap_time_start * (1 - car_power)
    for lap in race_data:
        
        #pobieranie danych pogody i usterek w danym okrążeniu
        

        weather = lap["lap_data"]["weather"]
        failure = failure_generator(car_power,weather,tire_wear,parts_wear)
        
        #pobreanie obiektu z nazwy
        # failure = get_failure_by_name(failure,CarFailure.load_from_file(failure_list))
        if failure:
            failures_list.append(failure)

        lap_number = lap['lap_number']
        #obliczenie czasu okrążenia
        lap_time = lap_time_with_actuall_conditions(failures_list,lap_time_start,tires,tire_wear,weather,car_power,parts_wear)
        fix_engine = False
        fix_brakes = False
        fix_suspension = False
        tire_change = False
        fuel = False
        pit_stop = False
        # Sprawdzenie warunków zjazdu do pitstopu
        if fuel_level < fuel_pitstop or tire_wear < tire_wear_str:
            tire_change = True
            fuel = True
            pit_stop = True
        
        if parts_wear['Engine'] < engine_wear_strat:
            fix_engine = True
            pit_stop = True

        if parts_wear['Brakes'] < brakes_wear_strat:
            fix_brakes = True
            pit_stop = True

        if parts_wear['Suspension'] < suspension_wear_strat:  
            fix_suspension = True
            pit_stop = True

        if pit_stop:
            tires,tire_wear,failures_list, pitstop_time,fuel_level,pitstop_data, parts_wear = pitstop(car, tires,tire_wear,fuel_level, failures_list,fix_engine,fix_suspension, fix_brakes,tire_change,fuel ,parts_wear)
        

        else:
            pitstop_time = 0
        # elif parts_wear['Engine'] < engine_wear_strat:
        #     if parts_wear['Brakes'] < brakes_wear_strat:
        #         fix_brakes = True
        #     if parts_wear['Suspension'] < suspension_wear_strat:  
        #         fix_suspension = True
        #     fix_engine = True
        #     tires,tire_wear,failures_list, pitstop_time,fuel_level,pitstop_data = pitstop(car, tires,fuel_level, failures_list,repair = True,tire_change = True,fuel = True)
        
        # elif parts_wear['Suspension'] < suspension_wear_strat:
        #     if parts_wear['Brakes'] < brakes_wear_strat:
        #         fix_brakes = True
        #     fix_suspension = True
        #     tires,tire_wear,failures_list, pitstop_time,fuel_level,pitstop_data = pitstop(car, tires,fuel_level, failures_list,repair = True,tire_change = True,fuel = True)
        # elif parts_wear['Brakes'] < brakes_wear_strat:
        #     fix_brakes = True
            
        #     tires,tire_wear,failures_list, pitstop_time,fuel_level,pitstop_data = pitstop(car, tires,fuel_level, failures_list,repair = True,tire_change = True,fuel = True)

        
        
        total_time += lap_time + pitstop_time
        tire_wear -= tires_degrad
        fuel_level -= car.average_fuel_consumption * car_power
        
        parts_wear = {part: parts_wear[part] - parts_degrad.get(part, 0) for part in parts_wear}
    #fajnie by było tu wyświetlać która to była kalkulacja
    print("Calculation nr: ")
    return total_time


def failure_generator(car_power,weather,tire_wear,parts_wear):
    
    possible_failures_breaks = []
    possible_failures_engine = []
    possible_failures_suspension = []
    engine_wear = parts_wear['Engine']
    suspension_wear = parts_wear['Suspension']
    brakes_wear = parts_wear['Brakes']

    lst_fail_b = []
    lst_fail_e = []
    lst_fail_s = []

    random_failure = []

    for threshold in thresholds_brakes:
        if threshold[1] > brakes_wear:
            possible_failures_breaks.append(threshold[0])
    
    for threshold in thresholds_engine:
        if threshold[1] > engine_wear:
            possible_failures_engine.append(threshold[0])
    
    for threshold in thresholds_suspension:
        if threshold[1] > suspension_wear:
            possible_failures_suspension.append(threshold[0])
    
    if possible_failures_breaks:
        for name in possible_failures_breaks:
            lst_fail_b.append(get_failure_brakes_by_name(name)) 
            random_failure.append(choose_random_failure(lst_fail_b,parts_wear['Brakes']))

    if possible_failures_engine:
        for name in possible_failures_engine:
            lst_fail_e.append(get_failure_engine_by_name(name)) 
            random_failure.append(choose_random_failure(lst_fail_e,parts_wear['Engine']))
    
    if possible_failures_suspension:
        for name in possible_failures_suspension:
            lst_fail_s.append(get_failure_suspension_by_name(name))
            random_failure.append(choose_random_failure(lst_fail_s,parts_wear['Suspension']))

    

    # failure_prob = 1 - np.exp(-5 * car_power)
    # failure_prob = car_power - 0.4
    # random_failure = []
    
    # failure = random.choices([True, False], weights=[failure_prob, 1 - failure_prob], k=1)[0]
    # if failure:
    #     random_failure = []
    #     failures = CarFailure.load_from_file(failure_list)
    #     random_failure.append(choose_random_failure(failures))
    # else:
    #     random_failure = None    
    
    tire_fail_prob = (1 - tire_wear)**2
    tire_failure = random.choices([True, False], weights=[tire_fail_prob, 1 - tire_fail_prob], k=1)[0]

    if tire_failure:
        if not random_failure:
            random_failure = []
        tire_fail = random.choices(["Tire puncture","Tire blowout"], weights=[tire_wear, 1 - tire_wear], k=1)[0]
        tire_fail = get_failure_tires_by_name(tire_fail)
        random_failure.append(tire_fail)


    
    return random_failure

def choose_random_failure(failures,part_wear):
    
    probabilities = [failure.propability for failure in failures]
    weights = np.array(probabilities) * (1 - part_wear)
    chosen_failure = random.choices(failures, weights, k=1)[0]
    
    return chosen_failure


def abc_algorithm_demo(max_iter, num_bees, food_limit):
    # Parametry algorytmu
    dim = 7  # Liczba wymiarów
    num_bees = 50  # Liczba pszczół
    max_iter = 50  # Maksymalna liczba iteracji
    food_limit = 25  # Limit wyczerpania źródła pożywienia
    best_strategies = []
    bounds = [
        [round(x, 2) for x in [i * 0.01 for i in range(10, 101)]], # Strategia hamulce
        [round(x, 2) for x in [i * 0.01 for i in range(10, 101)]], #Strategia silnik
        [round(x, 2) for x in [i * 0.01 for i in range(10, 101)]], #Strategia zawieszenie
        ['soft', 'medium', 'hard', 'wet'],  # Strategia opon
        (1, 35),  # Strategia paliwa
        [round(x, 2) for x in [i * 0.01 for i in range(10, 101)]],  # Zużycie opon
        [round(x * 0.05 + 0.5, 2) for x in range(11)] #Limit mocy pojazdu
    ]
    
    # Inicjalizacja
    population = [
        [
            random.choice(bounds[0]), # Strategia hamulce
            random.choice(bounds[1]), #Strategia silnik
            random.choice(bounds[2]),  #Strategia zawieszenie
            random.choice(bounds[3]),  # Strategia opon
            random.randint(*bounds[4]),  # Strategia paliwa
            random.choice(bounds[5]),  # Strategia zużycia opon
            random.choice(bounds[6]) #Strategia mocy pojazdu
        ]
        for _ in range(num_bees)
    ]

    fitness = [calculate_total_time(race_data, strategy) for strategy in population]
    trial_counter = np.zeros(num_bees)
    
    best_fitness = min(enumerate(fitness), key=lambda x: x[1])
    best_strategies.append(population[best_fitness[0]])
    best_solutions = [best_fitness[1]]
    best_fitness = best_fitness[1]
    

    # Główna pętla algorytmu
    for _ in range(max_iter):
        # Faza pszczół robotnic
        for i in range(num_bees):
            partner = random.randint(0, num_bees - 1)
            phi = np.random.uniform(-1, 1)
            candidate = []
            for j in range(dim):
                if j == 3:  # Strategia opon (string)
                    candidate.append(random.choice(bounds[3]))
                # elif j == 0:
                #     candidate_value = population[i][j] + phi * (population[i][j] - population[partner][j])
                #     candidate_value = max(bounds[j][0], min(candidate_value, bounds[j][1]))
                #     candidate.append(int(round(candidate_value)))
                elif j == 6:
                    candidate_value = population[i][j] + phi * (population[i][j] - population[partner][j])
                    candidate_value = max(bounds[j][0], min(candidate_value, bounds[j][1]))  # Klipowanie
                    candidate_value = round(candidate_value * 2) / 2  
                    candidate.append(candidate_value)
                elif j in range(0,3) or j == 4:
                    candidate_value = population[i][j] + phi * (population[i][j] - population[partner][j])
                    candidate_value = max(bounds[j][0], min(candidate_value, bounds[j][1]))  # Klipowanie
                    candidate_value = round(candidate_value * 2) / 2  
                    candidate.append(candidate_value)
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
                if j == 3:  # Strategia opon (string)
                    candidate.append(random.choice(bounds[3]))
                # elif j == 0:
                #     candidate_value = population[selected][j] + phi * (population[selected][j] - population[partner][j])
                #     candidate_value = max(bounds[j][0], min(candidate_value, bounds[j][1]))
                #     candidate.append(int(round(candidate_value)))
                elif j in range(0,3) or j == 4:
                    candidate_value = population[i][j] + phi * (population[i][j] - population[partner][j])
                    candidate_value = max(bounds[j][0], min(candidate_value, bounds[j][1]))  # Klipowanie
                    candidate_value = round(candidate_value * 2) / 2  
                    candidate.append(candidate_value)
                elif j == 6:
                    candidate_value = population[selected][j] + phi * (population[selected][j] - population[partner][j])
                    candidate_value = max(bounds[j][0], min(candidate_value, bounds[j][1]))  # Klipowanie
                    candidate_value = round(candidate_value * 2) / 2  # Zaokrąglenie do 0.5
                    candidate.append(candidate_value)
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
                    random.choice(bounds[0]), # Strategia hamulce
                    random.choice(bounds[1]), #Strategia silnik
                    random.choice(bounds[2]),  #Strategia zawieszenie
                    random.choice(bounds[3]),  # Strategia opon
                    random.randint(*bounds[4]),  # Strategia paliwa
                    random.choice(bounds[5]),  # Strategia zużycia opon
                    random.choice(bounds[6]) #Strategia mocy pojazdu
                ]
                fitness[i] = calculate_total_time(race_data, population[i])
                trial_counter[i] = 0

        # Zapis najlepszych wyników
        current_best = min(enumerate(fitness), key=lambda x: x[1])

        idx = current_best[0] 

        current_best = current_best[1]

        if current_best < best_fitness:
            best_fitness = current_best
        best_strategies.append(population[idx])
        best_solutions.append(best_fitness)

    # Wizualizacja wyników (opcjonalnie)
    # visualize_optimization(population, calculate_total_time, lb, ub, best_solutions)
    for i, value in enumerate(best_strategies, start=1):  
        print(f"Strategia {i}: {value}")
    print(best_solutions)
    return best_solutions


def pitstop(car, tires,tires_wear,fuel_level, actuall_failures,fix_engine,fix_suspension, fix_brakes,tire_change,fuel ,parts_wear):
    """
    Funkcja symulująca pitstop: wymiana opon, naprawa usterek, uzupełnienie paliwa.
    """
    total_repair_time = 0
    tires_change_time = 0
    t_to_garage = 0
    time_eng = 0
    time_brak = 0
    time_sus = 0
    time_refuel = 0
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
        time_refuel = 10 + refuel * 2 #czas spędzony na dolanie x litrów paliwa
        fuel_level = car.fuel_tank_capacity

    if fix_engine:
    
        time_eng = 300
        parts_wear["Engine"] = 1
    
    if fix_brakes:
        
        time_brak = 340
        parts_wear["Brakes"] = 1
    if fix_suspension:
        
        time_sus = 460
        parts_wear["Suspension"] = 1
    failure_names = []
    if actuall_failures:
    # Naprawa usterek
       
        for failure in actuall_failures:
            
            failure_names.append(failure[0].name)
            total_repair_time += failure[0].fixtime  # Sumujemy czas naprawy

    # Można zresetować awarie po naprawach
        actuall_failures.clear()
        t_to_garage = 60
    
    # Pitstop trwa również określony czas
    pitstop_time = 90 + total_repair_time + time_refuel + tires_change_time + t_to_garage + time_sus + time_brak + time_eng # Zliczamy czas pitstopu i naprawy
    
    # pitstop_data = {
    #     "repairs" : failure_names,
    #     "fuel_amount" : refuel,
    #     "tires_change" : tire_change,
    #     "time in pitstop" : pitstop_time

    # }
    pitstop_data = None
    # Zwracamy nowe opony, czas pitstopu oraz naprawy
    try:
        return tires.name,tires_wear,actuall_failures, pitstop_time,fuel_level,pitstop_data,parts_wear
    except:
        return tires,tires_wear,actuall_failures, pitstop_time,fuel_level,pitstop_data,parts_wear

def lap_time_with_actuall_conditions(actuall_failures,lap_time,tires,tires_wear,weather,car_power,parts_wear):
    #zwiększenie czasu okrążenia ze względu na usterki
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
    #procentowe zwiększenie czasu okrazenia w zwiazku z mokroscia jezdzni 
    if wet_level > 0:
        wet_reduction = wet_level - tires_wet_cap
        if wet_reduction < 0:
            wet_reduction = 0

    
    grip_tires = tires.grip
    grip_weather = weather.surface_grip

    #zwiększenie czasu okrążenia ze względu na typ użytych opon przy aktualnej pogodzie
    grip_red = grip_weather - grip_tires
    if grip_red < 0:
        grip_red = 0

    parts_sum_wear = 1 - sum(parts_wear.values())


    return lap_time + lap_time * max_red + lap_time * wet_reduction + lap_time * grip_red + lap_time * (1 - tires_wear) + lap_time * (parts_sum_wear / 3)

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

def get_failure_engine_by_name(name,failure_list=failures_engine):
    for failure in failure_list:
        if  failure.name.lower() == name.lower():  # Ignoruje wielkość liter
            return failure
    return None

def get_failure_suspension_by_name(name,failure_list=failures_suspension):
    for failure in failure_list:
        if  failure.name.lower() == name.lower():  # Ignoruje wielkość liter
            return failure
    return None

def get_failure_tires_by_name(name,failure_list=failures_tires):
    for failure in failure_list:
        if  failure.name.lower() == name.lower():  # Ignoruje wielkość liter
            return failure
    return None

def get_failure_brakes_by_name(name,failure_list=failures_brakes):
    for failure in failure_list:
        if  failure.name.lower() == name.lower():  # Ignoruje wielkość liter
            return failure
    return None


def get_weather_by_name(name,weather_list):
    for weather in weather_list:
        if  weather.name.lower() == name.lower():  # Ignoruje wielkość liter
            return weather
    return None  


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

def monitor_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / (1024 ** 2)  # Zwraca pamięć w MB
# Uruchomienie algorytmu
if __name__ == "__main__":
    start_memory = monitor_memory()
    start_time = time.perf_counter()
    abc_algorithm_demo(50, 10, 50)
    stop_time = time.perf_counter()
    end_memory = monitor_memory()

    print(f"Memory used: {end_memory - start_memory:.2f} MB")
    print(f"Execution time: {stop_time - start_time}")

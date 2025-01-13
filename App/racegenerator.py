import random
import json
import os
from race_car import RaceCar
from race_track import RaceTrack
from car_failure import CarFailure
from weather_class import Weather
from tires_class import Tire
weather_list_json = 'data/weather_conditions.json'

def lap_generator(car,track,failure_list,race_time,drive_style,weather,tires):
    
    lap_events = []
    if race_time in range(14400,57600):
        night = True
    else:
        night = False
    
    weather = weather_generator(weather)
    lap_events.append(weather)

    if drive_style == 0:
        if not night:
            failure_prob = 0.2
        if night:
            failure_prob = 0.25
    if drive_style == 1:

        if not night:
            failure_prob = 0.3
        if night:
            failure_prob = 0.40

    if drive_style == 2:
        if not night:
            failure_prob = 0.4
        if night:
            failure_prob = 0.60

    
    
    failure = random.choices([True, False], weights=[failure_prob, 1 - failure_prob], k=1)[0]
    if failure:
        random_failure = []
        failures = CarFailure.load_from_file(failure_list)
        random_failure = choose_random_failure(failures)
        lap_events.append(random_failure)
    else:
        lap_events.append(None)
    

    
    return lap_events

def weather_generator(actual_weather):
    options = [actual_weather.name] + actual_weather.next_weather
    next_weather = random.choices(options,weights=[0.7,0.15,0.15],k=1)[0]
    return get_weather_by_name(next_weather,Weather.load_from_file(weather_list_json))


def get_weather_by_name(name,weather_list):
    for weather in weather_list:
        if  weather.name.lower() == name.lower():  # Ignoruje wielkość liter
            return weather
    return None  

def save_to_json_race(file_path, lap_number, lap_data):
    # Check if the file exists
    if os.path.exists(file_path):
        # If it exists, load its contents
        with open(file_path, 'r') as file:
            race_data = json.load(file)
            # Ensure the race data is a list, not a dictionary
            if not isinstance(race_data, list):
                race_data = []  # If the loaded data is not a list, reset it as an empty list
    else:
        # If it doesn't exist, create a new list
        race_data = []

    # Create a dictionary for the current lap with the lap_number as a key
    lap_entry = {"lap_number": lap_number, "lap_data": lap_data}

    # Append the current lap data to the list
    race_data.append(lap_entry)

    # Save the updated list back to the file
    with open(file_path, 'w') as file:
        json.dump(race_data, file, indent=4)

def choose_random_failure(failures):
    
    probabilities = [failure.propability for failure in failures]
    chosen_failure = random.choices(failures, weights=probabilities, k=1)[0]
    
    return chosen_failure

def lap_time_with_actuall_conditions(actuall_failures,lap_time,tires,tires_wear,weather):
    reductions = None
    if actuall_failures:
        reductions = [failure.speed_reduction for failure in actuall_failures]
    max_red = 0
    if reductions:
        max_red = max(reductions)

    wet_level = weather.wet

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

    

    return lap_time + lap_time * max_red + lap_time * wet_reduction + lap_time * grip_red + lap_time * tires_wear
        
def get_tire_by_name(tires, name):
    for tire in tires:
        if tire.name.lower() == name.lower():  # Ignoruje wielkość liter
            return tire
    return None  # Jeśli nie znaleziono opony


def fuel_level_fun(fuel_level,fuel_consumption,actuall_failures):
    fuel_penalty = [failure.fuel_penalty for failure in actuall_failures]
    fuel_penalty = sum(fuel_penalty)
    return fuel_level - fuel_consumption - fuel_consumption*fuel_penalty

def pitstop(car, tires,fuel_level, actuall_failures,repair = True,tire_change = True,fuel = True):
    """
    Funkcja symulująca pitstop: wymiana opon, naprawa usterek, uzupełnienie paliwa.
    """
    total_pit_time = 0
    if tire_change:
    # Wymiana opon na nowe (przywracamy pełną wydajność)
        tires_list = 'data/tires_characteristics.json'
        tires_list = Tire.load_from_file(tires_list)
        
        new_tire = get_tire_by_name(tires_list,tires)
        tires = new_tire

        tires_wear = 1
        tires_change_time = 20
    
    # Uzupełnienie paliwa
    if fuel:
        refuel = car.fuel_tank_capacity - fuel_level  # Maksymalna pojemność baku
        time_refuel = 10 + refuel * 2
        fuel_level = car.fuel_tank_capacity
    
    failure_names = []
    if repair:
    # Naprawa usterek
        total_repair_time = 0
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
    return tires,tires_wear,actuall_failures, pitstop_time,fuel_level,pitstop_data


def clear_json_file(file_path):
    # Open the file in write mode to overwrite its contents
    with open(file_path, 'w') as file:
        # Write an empty dictionary to the file (this clears it)
        json.dump({}, file, indent=4)
        # If you need to reset to an empty list, use `[]` instead of `{}`.
        # json.dump([], file, indent=4)

# Example usage:

def main():
    clear_json_file('data/race_simulation1.json')
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
    track = RaceTrack()
    tires_list_json = 'data/tires_characteristics.json'
    tires_list = Tire.load_from_file(tires_list_json)
    
    weather_list = 'data/weather_conditions.json'
    
    tires = get_tire_by_name(tires_list,"soft")
    
    weathers = Weather.load_from_file(weather_list)
    weather = weathers[0]

    actuall_failures = []
    #lap data słownik
    keys = ["lap_time", "fuel_level", "tire_wear", "failure","weather","tires","pitstop"]
    lap_data = {key: None for key in keys}
    lap_data["pitstop"] = "No"


    lap_data["lap_time"] = car.lap_time
    lap_data["fuel_level"] = car.fuel_tank_capacity
    lap_data["tire_wear"] = 1
    lap_data["tires"] = tires.name
    lap_data["pitstop"] = "No"
    
    tires_wear = 1
    fuel_level = car.fuel_tank_capacity
    failure_list = 'data/failure_list.json'
    i = 1
    race_time = 0
    while race_time < 86400:
    

        lap_data_gen = lap_generator(car,track,failure_list,race_time,1,weather,tires)
        try:
            lap_data["failure"] = lap_data_gen[1].name
        except:
            lap_data["failure"] = "No failure"
        lap_data["weather"] = lap_data_gen[0].name
        
        weather = lap_data_gen[0]

        if lap_data_gen[1]:
            actuall_failures.append(lap_data_gen[1])
        
        final_lap_time = lap_time_with_actuall_conditions(actuall_failures,car.lap_time,tires,tires_wear,weather)
        tires_wear = tires_wear - tires.degradation_rate
        
        
        
        
        fuel_level = fuel_level_fun(fuel_level,car.average_fuel_consumption,actuall_failures)
        
        
        
        race_time += final_lap_time
        pitstop_time = 0
        if tires_wear <= 0.5 or fuel_level <= 5:
            tires_name = "soft"
            tires,tires_wear,actuall_failures, pitstop_time,fuel_level,pitstop_data = pitstop(car,tires_name,fuel_level,actuall_failures)
            lap_data["pitstop"] = pitstop_data
        else:
            lap_data["pitstop"] = "No"
        lap_data["tires"] = tires.name
        lap_data["fuel_level"] = fuel_level
        lap_data["tire_wear"] = tires_wear
        
        final_lap_time += pitstop_time
        lap_data["lap_time"] = final_lap_time
        save_to_json_race('data/race_simulation1.json',i,lap_data)

        i += 1

main()
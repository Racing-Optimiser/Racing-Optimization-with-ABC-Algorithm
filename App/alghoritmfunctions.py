import car_failure
import random
import json
from car_failure import CarFailure


# Wczytaj dane z pliku JSON
with open("race_simulation.json", "r") as file:
    race_data = json.load(file)
for lap in race_data:
        print(lap['lap_number'])
        lap_time = lap["lap_data"]["lap_time"]
        tire_wear = lap["lap_data"]["tire_wear"]
        fuel_level = lap["lap_data"]["fuel_level"]
        failure = lap["lap_data"]["failure"]
        weather = lap["lap_data"]["weather"]
        

def calculate_total_time(race_data, strategy):
    total_time = 0
    for lap in race_data:
        lap_time = lap["lap_data"]["lap_time"]
        tire_wear = lap["lap_data"]["tire_wear"]
        fuel_level = lap["lap_data"]["fuel_level"]
        failure = lap["lap_data"]["failure"]
        weather = lap["lap_data"]["weather"]
        
        # Adjust lap time for tire wear and weather conditions
        adjusted_lap_time = lap_time + (tire_wear * 10)  # Increase time for tire wear
        if weather == "Light rain":
            adjusted_lap_time += 15  # Time penalty for rain
        
        # Check if a pitstop is required (e.g. fuel or tire change)
        if fuel_level < 5 or tire_wear < 0.5 or "overheat" in failure:
            pitstop_time = perform_pitstop(failure, strategy)  # Time spent in pitstop
            adjusted_lap_time += pitstop_time
        
        total_time += adjusted_lap_time
    
    return total_time

def perform_pitstop(failure, strategy):
    # Assume pitstop times and repairs for the sake of the example
    repair_times = {
        "Fuel pump issue": 60,
        "Brakes overheat": 80,
        "Cooling system": 70,
        "Paint scratch": 20
    }
    
    total_repair_time = sum([repair_times.get(f, 0) for f in failure.split(',')])
    tire_change_time = 30 if strategy["tires_change"] else 0
    fuel_time = 20 if strategy["fuel_amount"] > 10 else 0
    
    return total_repair_time + tire_change_time + fuel_time



def choose_random_failure(failures):
    
    probabilities = [failure.propability for failure in failures]
    chosen_failure = random.choices(failures, weights=probabilities, k=1)[0]
    
    return chosen_failure



# filename = "failure_list.json"  
# failures = CarFailure.load_from_file(filename)


# random_failure = choose_random_failure(failures)

# print(f"Wybrana usterka: {random_failure.name}")
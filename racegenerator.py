import alghoritmfunctions
import car_failure
import race_car
import race_track
import json
from alghoritmfunctions import choose_random_failure
from race_car import RaceCar
from race_track import RaceTrack
from car_failure import CarFailure






def race_generator(car,track,failure_list):
    
    race_events = {}
    for i in range(track.lap_amount + 1):
        random_failure = []
        failures = CarFailure.load_from_file(failure_list)
        random_failure = choose_random_failure(failures)
        race_events[i] = random_failure


def main():
    car = RaceCar(
    make="Toyota",
    model="GR010 Hybrid",
    top_speed=340,
    horsepower=680,
    weight=1040,
    fuel_tank_capacity=35,
    average_fuel_consumption=40,
    )
    track = RaceTrack()


    failure_list = 'failure_list.json'
    race_generator(car,track,failure_list)

main()
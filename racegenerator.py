import random
from alghoritmfunctions import choose_random_failure
from race_car import RaceCar
from race_track import RaceTrack
from car_failure import CarFailure


def lap_generator(car,track,failure_list,race_time,drive_style,weather):
    
    
    if race_time in range(14400,57600):
        night = True
    else:
        night = False
    
    weather = weather_generator(weather)


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
        lap_events = random_failure
    
    return lap_events

def weather_generator(actual_weather):
    
    next_weather = random.choices(actual_weather.next_weather,weights=[0.5,0.5],k=1)[0]
    return next_weather




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
    lap_generator(car,track,failure_list)

main()
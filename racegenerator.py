import random
from alghoritmfunctions import choose_random_failure
from race_car import RaceCar
from race_track import RaceTrack
from car_failure import CarFailure
from weather_class import Weather

def lap_generator(car,track,failure_list,race_time,drive_style,weather):
    
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
    
    return lap_events

def weather_generator(actual_weather):
    options = [actual_weather.name] + actual_weather.next_weather
    next_weather = random.choices(options,weights=[0.7,0.15,0.15],k=1)[0]
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

    weather_list = 'weather_conditions.json'
    weathers = Weather.load_from_file(weather_list)
    weather = weathers[0]


    failure_list = 'failure_list.json'
    for i in range(track.lap_amount):

        lap_events = lap_generator(car,track,failure_list,5,1,weather)
        weather = lap_events[0]
        actuall_failures = lap_events[1]
main()
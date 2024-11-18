import alghoritmfunctions
import CarFailure
import RaceCar
import json

failure_list = CarFailure.load_from_file('failure_list.json')

car = RaceCar(
    make="Toyota",
    model="GR010 Hybrid",
    top_speed=340,
    horsepower=680,
    weight=1040,
    fuel_tank_capacity=35,
    average_fuel_consumption=40,
)





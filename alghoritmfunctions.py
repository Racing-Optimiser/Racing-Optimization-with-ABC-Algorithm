import CarFailure
import random
import json


failure_list = CarFailure.load_from_file('failure_list.json')

def pit_stop_time(am_of_fuel,failure = None,wheels = False):
    #time to switch wheels
    tw = 20
    #time to take car in and out of garage
    t_grg = 60
    #time lost to drive to pit-stop
    t_drp = 20
    #time spend on refueling 1 l of fuel
    tf = 2
    
    if not wheels:
        tw = 0
    
    if not failure:
        t_p = tw + tf * am_of_fuel + t_drp
    
    elif failure.garage:
        t_p = t_grg + failure.time + tw + tf * am_of_fuel + t_drp
    
    else:
        if tf * am_of_fuel > failure.time:
            t_p = am_of_fuel + t_drp
        else:
            t_p = failure.time + t_drp
    
    return t_p
    
    
def tire_wear():
    pass


def choose_random_failure(failures):
    
    probabilities = [failures.propability]
    chosen_failure = random.choices(failures, weights=probabilities, k=1)[0]
    
    return chosen_failure



# filename = "failure_list.json"  
# failures = CarFailure.load_from_file(filename)


# random_failure = choose_random_failure(failures)

# print(f"Wybrana usterka: {random_failure.name}")
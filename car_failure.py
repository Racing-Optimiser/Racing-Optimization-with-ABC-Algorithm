import json
import random

class CarFailure:
    name: str
    fixtime : int #sec
    garage: bool #
    stock_number: int #ile razy można ponownie naprawić daną usterkę
    propability : float #prawdopowobienstwo wystapienia(waga)
    speed_reduction: float #procent vmax
    speed_reduction_night : float #procent vmax w nocy
    failure_deterioration : float #pogarszanie sie usterki per ?okrazenie?
    next_failure : str #nastepna usterka gdy nie naprawione
    fuel_penalty : float #zwiekszone zuzycie paliwa 1l/100km
    chance_of_repair_failure : float #szansa na nieudaną naprawę
    

    def __init__(self,name,fixtime,garage,stock_number,propability,speed_reduction,speed_reduction_night,failure_deterioration,next_failure,fuel_penalty,chance_of_repair_failure) -> None:

        self.name = name
        self.fixtime = fixtime
        self.garage = garage
        self.stock_number = stock_number
        self.propability = propability
        self.speed_reduction = speed_reduction
        self.speed_reduction_night = speed_reduction_night
        self.failure_deterioration = failure_deterioration
        self.next_failure = next_failure
        self.fuel_penalty = fuel_penalty
        self.chance_of_repair_failure = chance_of_repair_failure
        


    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            failures = []
            for item in data:
                failure = CarFailure(
                    name=item["name"],
                    fixtime=item["fixtime"],
                    garage=item["garage"] == "True",
                    stock_number=item["stock_number"],
                    propability=item["propability"],
                    speed_reduction=item["speed_reduction"],
                    speed_reduction_night = item["speed_reduction_night"],
                    failure_deterioration=item["failure_deterioration"],
                    next_failure=item["next_failure"],
                    fuel_penalty=item["fuel_penalty"],
                    chance_of_repair_failure=item['chance_of_repair_failure']
                )
                failures.append(failure)
            return failures



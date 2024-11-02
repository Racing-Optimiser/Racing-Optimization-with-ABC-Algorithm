import json
import random

class CarFailure:
    name: str
    fixtime : int #sec
    garage: bool
    crucial: bool
    stock_number: int
    propability : float
    speed_reduction: float
    failure_deterioration : float
    next_failure : str

    def __init__(self,name,fixtime,garage,crucial,stock_number,propability,speed_reduction,failure_deterioration,next_failure) -> None:

        self.name = name
        self.fixtime = fixtime
        self.garage = garage
        self.crucial = crucial
        self.stock_number = stock_number
        self.propability = propability
        self.speed_reduction = speed_reduction
        self.failure_deterioration = failure_deterioration
        self.next_failure = next_failure
        


    @staticmethod
    def load_from_file(self,filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            failures = []
            for item in data:
                failure = CarFailure(
                    name=item["name"],
                    fixtime=item["fixtime"],
                    garage=item["garage"] == "True",
                    crucial=item["crucial"] == "True",
                    stock_number=item["stock_number"],
                    propability=item["propability"],
                    speed_reduction=item["speed_reduction"],
                    failure_deterioration=item["failure_deterioration"],
                    next_failure=item["next_failure"]
                )
                failures.append(failure)
            return failures

def choose_random_failure(failures):
    
    probabilities = [failures.propability]
    chosen_failure = random.choices(failures, weights=probabilities, k=1)[0]
    
    return chosen_failure


filename = "failure_list.json"  
failures = CarFailure.load_from_file(filename)


random_failure = choose_random_failure(failures)

print(f"Wybrana usterka: {random_failure.name}")

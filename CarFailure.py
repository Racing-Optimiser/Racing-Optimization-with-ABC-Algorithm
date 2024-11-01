import json

class CarFailure:
    name: str
    fixtime : int #sec
    garage: bool
    crucial: bool
    stock_number: int

    def __init__(self) -> None:

        # self.part = part
        pass


    @staticmethod
    def load_from_file(self,filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data

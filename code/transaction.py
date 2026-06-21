'''code/transaction.py'''

class Transaction:
    def __init__(self, type: str, date, employee) -> None:
        self.type = type  # 1: Abastecimento / 2: Retirada 
        self.date = date
        self.employee = employee
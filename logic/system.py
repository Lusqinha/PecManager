from database.transfers import TransfersManager

class PecuniaryManager(TransfersManager):
    def __init__(self):
        super().__init__()
        self.currency = 0
        self.calculate_currency()
        
    def calculate_currency(self):
        all_transfers = self.get_all()
        self.currency = 0
    
        for transfer in all_transfers:
            if transfer['category'] == 'entrada':
                self.currency += transfer['value']
            elif transfer['category'] == 'saida':
                self.currency -= transfer['value']
    


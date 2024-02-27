from controller.manager import TransferManager

class PecuniaryManager:
    def __init__(self):
        self.transfers = TransferManager()
        self.cashier = 0
        
    def calculate_cashier(self):
        all_transfers = self.transfers.get_all()
        self.cashier = 0
        
        for transfer in all_transfers:
            if transfer['category'] == 'entrada':
                self.cashier += transfer['value']
            elif transfer['category'] == 'saida':
                self.cashier -= transfer['value']
    
from controller.core import Controller

class TransferManager(Controller):
    def __init__(self):
        super().__init__("transfers",{
            "date": str,
            "value": float,
            "description": str,
            "category": str
        })

            
        
    
from tinydb import Query, where
from database.db_start import Database
"""
    This class is responsible for managing the database of transfers.
"""

class TransfersManager:
    def __init__(self):
        self.table = Database.table('transfers')
        self.local_query = Query()
    
    def match_model(self, data:dict):
        try:
            model = self.show_model_data()
            if set(data.keys()) != set(model.keys()):
                return False

            for key in model.keys():
                if type(data[key]) != model[key]:
                    return False
            
            return True
        except Exception as e:
            print(e)
            return False, e
    
    def insert(self, data:dict):
        try:
            match = self.match_model(data)
            if match:
                self.table.insert(data)
                return True
            else:
                print('Data not match with model')
                return False
            
        except Exception as e:
            print(e)
            return False, e
    
    def get_all(self):
        try:
            return self.table.all()
        except Exception as e:
            print(e)
            return False, e
    
    def get_by_date(self, date:str):
        try:
            return self.table.search(where('date') == date)
        except Exception as e:
            print(e)
            return False, e
    
    def get_by_category(self, category:str):
        try:
            return self.table.search(where('category') == category)
        except Exception as e:
            print(e)
            return False, e
    
    def delete(self, id):
        try:
            self.table.remove(self.local_query.id == id)
            return True
        except Exception as e:
            print(e)
            return False, e
        
    def custom_query(self, query):
        try:
            return self.table.search(query)
        except Exception as e:
            print(e)
            return False, e
    
    def show_model_data(self):
        model = {
            'date': str,
            'value': float,
            'description': str,
            'category': str,
        }
        return model
    
    

# Tests
def tests(data:dict):
    manager = TransfersManager()
    print(manager.show_model_data())
    print(manager.insert(data))
    print(manager.get_all())
    print(manager.get_by_date(data['date']))
    print(manager.get_by_category(data['category']))
    print(manager.custom_query(where('category') == data['category']))
    print(manager.get_all())

if __name__ == "__main__":
    tests({
        'date': '30-12-2022',
        'value': 30.0,
        'description': 'Online purchase',
        'category': 'saida'
    })
from tinydb import Query, where
from tinydb.table import Document
from database.db_start import Database


class CantMatchModel(Exception):
    pass


def match_model(data: dict, model: dict) -> bool:
    try:
        if set(data.keys()) != set(model.keys()):
            return False

        for key in model.keys():
            if type(data[key]) != model[key]:
                return False

        return True
    except Exception as e:
        raise CantMatchModel(e)


class Controller:
    def __init__(self, table: str, model: dict):
        self.table = Database.table(table)
        self.local_query = Query()
        self.model = model

    def insert(self, data: dict) -> bool:
        try:
            match_data = match_model(data, self.model)

            if match_data:
                self.table.insert(data)
                return True

            return False
        except Exception as e:
            print(e)
            return False

    def remove(self, id: int) -> bool:
        try:
            self.table.remove(self.local_query.id == id)
            return True
        except Exception as e:
            print(e)
            return False

    def get_all(self) -> list:
        try:
            all_transfers = self.table.all()
            return all_transfers
        except Exception as e:
            print(e)
            return []

    def get(self, id: int) -> Document | None:
        try:
            item = self.table.get(self.local_query.id == id)

            if item and len(item) == 1:
                return item[0]

            return None

        except Exception as e:
            print(e)
            return None

    def get_filtered(self, filter: str, value: str) -> list:
        try:

            filtered = self.table.search(where(filter) == value)
            return filtered

        except Exception as e:
            print(e)
            return []

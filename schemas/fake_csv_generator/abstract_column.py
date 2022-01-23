from abc import ABC

class AbstractColumn(ABC):
    name: str

    def __init__(self, name, faker, next=None):
        self.name = name
        self.faker = faker
        self.next = next

    def generate_value(self):
        raise NotImplementedError

    def create_column_from_dict(self, column: dict):
        raise NotImplementedError





from abc import ABC
from faker import Faker


class AbstractColumn(ABC):
    """
    Base class for column instance
    """
    name: str

    def __init__(self, name: str, faker: Faker, next=None):
        """
        :param name: Name of the column
        :param faker: Faker for creating fake data
        :param next: Next column in chain of responsibility
        """
        self.name = name
        self.faker = faker
        self.next = next

    def generate_value(self):
        raise NotImplementedError

    def create_column_from_dict(self, column: dict):
        raise NotImplementedError





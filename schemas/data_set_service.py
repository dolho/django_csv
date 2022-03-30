import os
import time
from pathlib import Path
import time
from .models import Schema, DataSet
from django.conf import settings


class DataSetService():

    def __init__(self):
        self.__user_permission_checkers = [self.__is_regular_user_allowed_to_create_dataset]

    def get_data_sets(self, schema_id):
        datasets = DataSet.objects.filter(schema_id=schema_id)
        return datasets

    def path_to_file(self, directory, uuid):
        return os.path.join(directory, uuid + '.csv')

    def is_user_allowed_to_create_dataset(self, user, schema: Schema, amount_of_rows: int) -> bool:
        for check in self.__user_permission_checkers:
            if not check(user, amount_of_rows=amount_of_rows, schema=schema):
                return False
        return True

    def __is_regular_user_allowed_to_create_dataset(self, user, **additional_data) -> bool:
        schema = additional_data["schema"]
        amount = additional_data['amount_of_rows']
        if not user.is_regular_account:
            return True
        if not (amount <= settings.REGULAR_LIMIT_OF_DATASET_ROWS):
            return False
        amount_of_datasets = len(DataSet.objects.filter(schema_id=schema))
        if not(amount_of_datasets < settings.REGULAR_LIMIT_OF_DATASETS_PER_SCHEMA):
            return False
        return True

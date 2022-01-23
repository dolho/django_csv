import csv
from .abstract_column import AbstractColumn
from csv_creator.celery import app
from schemas.schema_service import SchemaService
from schemas.fake_csv_generator.columns import IntegerColumn, JobColumn, FullNameColumn
from faker import Faker
from time import time
import os


FAKER = Faker()
SCHEMA_SERVICE = SchemaService(IntegerColumn(0, 1, name='initial', faker=FAKER,
                               next=JobColumn(name='initial', faker=FAKER,
                               next=FullNameColumn(name='initial', faker=FAKER))))


@app.task
def generate_csv(schema_columns, time_of_creation, user_id, schema_id, amount=100):
    columns = SCHEMA_SERVICE.create_list_of_columns(schema_columns)
    schema_folder_path = SCHEMA_SERVICE.get_schema_folder_path(user_id, schema_id)
    try:
        os.makedirs(schema_folder_path, 0o777)
    except FileExistsError:
        pass
    csv_file_path = os.path.join(schema_folder_path, str(time_of_creation) + '.csv')

    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = [i.name for i in columns]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        generated_row = {}
        for i in range(0, amount):
            for j in columns:
                generated_row[j.name] = j.generate_value()
            writer.writerow(generated_row)

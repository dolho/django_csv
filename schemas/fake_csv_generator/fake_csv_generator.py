import csv
from csv_creator.celery import app
from schemas.schema_service import SchemaService
from schemas.models import DataSet, Schema
from schemas.columns.columns import IntegerColumn, JobColumn, FullNameColumn
from schemas.file_upload.cloudinary_uploader import CloudinaryFileUploader
from faker import Faker
from time import time
import os
import logging


FILE_UPLOADER = CloudinaryFileUploader()
FAKER = Faker()
SCHEMA_SERVICE = SchemaService(IntegerColumn(0, 1, name='initial', faker=FAKER,
                               next=JobColumn(name='initial', faker=FAKER,
                               next=FullNameColumn(name='initial', faker=FAKER))))
# DATASET_SERVICE = DataSetService()


@app.task(bind=True)
def generate_csv(self, schema_columns, user_id: int, schema_id: int, amount=100):
    columns = SCHEMA_SERVICE.create_list_of_columns(schema_columns)
    schema_folder_path = SCHEMA_SERVICE.get_schema_folder_path(user_id, schema_id)
    try:
        os.makedirs(schema_folder_path, 0o777)
    except FileExistsError:
        pass
    csv_file_path = os.path.join(schema_folder_path, self.request.id + '.csv')

    dataset = DataSet.objects.create(uuid=self.request.id,
                           time_of_creation=None, #time(),
                           path_to_file=None, #FILE_UPLOADER.return_link_to_file(self.request.id),
                           schema_id=Schema.objects.get(pk=schema_id))
    try:
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = [i.name for i in columns]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            generated_row = {}
            for i in range(0, amount):
                for j in columns:
                    generated_row[j.name] = j.generate_value()
                writer.writerow(generated_row)
        with open(csv_file_path, 'r', newline='') as csvfile:
            response = FILE_UPLOADER.upload(csvfile, resource_type="raw", public_id=self.request.id)
            dataset.path_to_file = response["url"]
            dataset.time_of_creation = response["created_at"]
            dataset.save()
    except Exception as e:
        logging.critical(e)
        dataset.delete()


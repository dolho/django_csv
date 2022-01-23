from schemas.fake_csv_generator.abstract_column import AbstractColumn
import os

class SchemaService:

    def __init__(self, column: AbstractColumn=None):
        self.__head_of_the_column_chain = column

    def create_list_of_columns(self, schema_columns):
        result = []
        for column in schema_columns:
            created_column = self.__head_of_the_column_chain.create_column_from_dict(column)
            result.append(created_column)
        return result

    def get_schema_folder_path(self, user_id, schema_id):
        return os.path.join('generated_csv_data_sets', str(user_id), str(schema_id))

from schemas.columns.abstract_column import AbstractColumn
import os
from django.conf import settings
from schemas.models import Schema
from accounts.models import CustomUser


class SchemaService:

    def __init__(self, column: AbstractColumn = None):
        self.__head_of_the_column_chain = column
        self.__user_permission_checkers = [self.__is_regular_user_allowed_to_create_schema]
        self.__user_edit_permission_checkers = [self.__is_regular_user_allowed_to_edit_schema]

    def create_list_of_columns(self, schema_columns) -> [AbstractColumn]:
        """
        Creates a list of Column objects, which inherit from AbstractColumn
        :param schema_columns:
        :return:
        """
        result = []
        for column in schema_columns:
            created_column = self.__head_of_the_column_chain.create_column_from_dict(column)
            result.append(created_column)
        return result

    def get_schema_folder_path(self, user_id: int, schema_id: int) -> str:
        return os.path.join('media/generated_csv', str(user_id), str(schema_id))

    def is_user_allowed_to_create_schema(self, user: CustomUser, amount_of_columns: int) -> bool:
        """
        A function to check if user is allowed to create new schema
        :param user: CustomUser
        :param amount_of_columns: integer
        :return:
        """
        for check in self.__user_permission_checkers:
            if not check(user, amount_of_columns=amount_of_columns):
                return False
        return True

    def __is_regular_user_allowed_to_create_schema(self, user: CustomUser, **additional_data) -> bool:
        if not user.is_regular_account:
            return True
        amount = additional_data.get('amount_of_columns', None)
        if not amount:
            return False
        if not (amount <= settings.REGULAR_LIMIT_OF_SCHEMA_COLUMNS):
            return False
        amount_of_schemas = len(Schema.objects.filter(author_id=user))
        print("amount of schemas ", amount_of_schemas)
        if not(amount_of_schemas < settings.REGULAR_LIMIT_OF_SCHEMAS):
            return False
        return True

    def is_user_allowed_to_edit_schema(self, user: CustomUser, amount_of_columns) -> bool:
        for check in self.__user_edit_permission_checkers:
            if not check(user, amount_of_columns=amount_of_columns):
                return False
        return True

    def __is_regular_user_allowed_to_edit_schema(self, user, **additional_data) -> bool:

        if not user.is_regular_account:
            return True
        amount = additional_data.get('amount_of_columns', None)
        if not amount:
            return False
        if amount <= settings.REGULAR_LIMIT_OF_SCHEMA_COLUMNS:
            return True
        return False

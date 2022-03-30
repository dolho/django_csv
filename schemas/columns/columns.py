from .abstract_column import AbstractColumn


class FullNameColumn(AbstractColumn):

    def generate_value(self):
        return self.faker.name()

    def create_column_from_dict(self, column: dict):
        """
        Expects, that column have key 'columnType' with value 'full_name'.
        :param column:
        :return:
        """
        if column.get('columnType', None) == 'full_name':
            return FullNameColumn(name=column['columnName'], faker=self.faker)
        else:
            if self.next:
                return self.next.create_column_from_dict(column)
            raise ValueError(f'Column structure is incorrect {column}')


class IntegerColumn(AbstractColumn):

    def __init__(self, count_from, count_to, *args, **kwargs):
        count_from = int(count_from)
        count_to = int(count_to)
        if count_from >= count_to:
            raise ValueError('count_from can\'t be greater or equal to count_to')
        self.__count_from = count_from
        self.__count_to = count_to
        super().__init__(*args, **kwargs)

    def generate_value(self):
        return self.faker.random_int(self.__count_from, self.__count_to)

    def create_column_from_dict(self, column: dict):
        """
        Expects, that column have key 'columnType' with value 'integer'.
        additionally expects to have keys 'from' and 'to'
        :param column:
        :return:
        """
        if column.get('columnType', None) == 'integer':
            count_from = column['from']
            count_to = column['to']
            return IntegerColumn(count_from, count_to, name=column['columnName'], faker=self.faker)
        else:
            if self.next:
                return self.next.create_column_from_dict(column)
            raise ValueError('Column structure is incorrect')


class JobColumn(AbstractColumn):

    def generate_value(self):
        return self.faker.job()

    def create_column_from_dict(self, column: dict):
        """
        Expects, that column have key 'columnType' with value 'job'.
        :param column:
        :return:
        """
        if column.get('columnType', None) == 'job':
            return JobColumn(name=column['columnName'], faker=self.faker)
        else:
            if self.next:
                return self.next.create_column_from_dict(column)
            raise ValueError('Column structure is incorrect')

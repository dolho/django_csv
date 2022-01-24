import os
import time
from pathlib import Path
import time


class DataSetService():

    def get_data_sets(self, directory) -> [(time, str)]:
        result = []
        try:
            for filename in os.scandir(directory):
                if filename.is_file():
                    name_without_extension = Path(filename).stem
                    time_of_file_creation = os.path.getctime(filename)
                    time_of_file_creation_timestamp = time.ctime(time_of_file_creation)

                    result.append((time_of_file_creation_timestamp, name_without_extension))
        except FileNotFoundError:
            pass
        return sorted(result, reverse=True)

    def path_to_file(self, directory, uuid):
        return os.path.join(directory, uuid + '.csv')

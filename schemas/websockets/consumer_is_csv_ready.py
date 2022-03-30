import json
from channels.generic.websocket import WebsocketConsumer
from csv_creator.celery import app
from schemas.websockets.event_monitor import CSVMonitorThread
from schemas.data_set_service import DataSetService
from schemas.schema_service import SchemaService
from schemas.models import DataSet
from time import time
import threading
import functools
from celery.result import AsyncResult


DATA_SET_SERVICE = DataSetService()
SCHEMA_SERVICE = SchemaService()

CSV_MONITOR = CSVMonitorThread(app)
x = threading.Thread(target=CSV_MONITOR.run)
x.start()

# class FunctionOnEventDispatcher:
#
#     def __int__(self):
#         self.__dispatcher = {
#             ""
#         }
#
#     def send(self, event):
#         pass
#
#     def __send_ready(self):
#         pass
#
#     def __send_processing(self):
#         pass


class IsCSVReadyConsumer(WebsocketConsumer):
    """
    Class for consuming websocket messages
    """

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        user_id = self.scope['user'].id
        print(text_data_json)
        if type == 'is_csv_ready':
            schema_id = text_data_json["payload"]["schema_id"]
            csv_dir = SCHEMA_SERVICE.get_schema_folder_path(user_id, schema_id)
            path_to_csv = DATA_SET_SERVICE.path_to_file(csv_dir, text_data_json["payload"]["data_set_id"])
            uuid = text_data_json["payload"]["data_set_id"]
            res = AsyncResult(uuid)
            func_processing = functools.partial(self.send,
                                                text_data= json.dumps({
                                                    'type': 'is_csv_ready',
                                                    'payload': {"status": "processing",
                                                                "id": uuid}}
                                                ))
            time_of_creation = DataSet.objects.get(pk=uuid).time_of_creation
            func_success = functools.partial(self.form_success_answer,
                                             uuid=uuid)
                                             # text_data= json.dumps({
                                             #     'type': 'is_csv_ready',
                                             #     'payload': {"status": "ready",
                                             #                 "id": uuid,
                                             #                 "time": time_of_creation.strftime("%m/%d/%Y, %H:%M:%S"),
                                             #                 "path": DataSet.objects.get(pk=uuid).path_to_file}})
                                             # )
            if res.ready():
                self.form_success_answer(uuid)
                # self.send(text_data=json.dumps({
                #         'type': 'is_csv_ready',
                #         'payload': {"status": "ready",
                #                     "id": uuid,
                #                     "time": DataSet.objects.get(pk=uuid).time_of_creation.strftime("%m/%d/%Y, %H:%M:%S"),
                #                     "path": DataSet.objects.get(pk=uuid).path_to_file}
                #     }))
                return
            else :
                func_processing()
            CSV_MONITOR.add_uuid_function_pair_success(uuid, func_success)
            CSV_MONITOR.add_uuid_function_pair_processing(uuid, func_processing)

    def form_success_answer(self, uuid):
        self.send(text_data=json.dumps({
            'type': 'is_csv_ready',
            'payload': {"status": "ready",
                        "id": uuid,
                        "time": DataSet.objects.get(pk=uuid).time_of_creation.strftime("%m-%d-%Y, %H:%M:%S"),
                        "path": DataSet.objects.get(pk=uuid).path_to_file}
        }))
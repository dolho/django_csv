import json
from channels.generic.websocket import WebsocketConsumer
from csv_creator.celery import app
from time import time

class IsCSVReadyConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print("Websockets worked, ", text_data_json)
        type = text_data_json['type']
        if type == 'is_csv_ready':
            if int(time()) % 2 == 0:
                self.send(text_data=json.dumps({
                    'type': 'is_csv_ready',
                    'payload': {"status": "ready",
                                "id": text_data_json["payload"]}
                }))
            else:
                self.send(text_data=json.dumps({
                    'type': 'is_csv_ready',
                    'payload': {"status": "processing",
                                "id": text_data_json["payload"]}
                }))
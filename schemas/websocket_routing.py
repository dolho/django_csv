from django.urls import re_path

from . import consumer_is_csv_ready

websocket_urlpatterns = [
    re_path(r'ws', consumer_is_csv_ready.IsCSVReadyConsumer.as_asgi()),
]

from django.contrib import admin
from django.urls import path, include
from .views import SchemaView, SchemaCreationView, DataSetCreationView, DataSetLoadView
from .consumer_is_csv_ready import IsCSVReadyConsumer

urlpatterns = [
    path('', SchemaView.as_view(), name='index'),
    path('schemas/', SchemaCreationView.as_view(), name="create_schema"),
    path('schemas/<int:schema_id>/data-sets/', DataSetCreationView.as_view(), name='create_data_set'),
    path('schemas/<int:schema_id>/data-sets/<str:timestamp>', DataSetLoadView.as_view(), name='load_data_set'),
    path('ws/', IsCSVReadyConsumer.as_asgi())
]

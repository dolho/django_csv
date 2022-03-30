from django.urls import path
from .views import SchemaView, SchemaCreationView,SchemaEditView, SchemaDeletionView, \
    DataSetCreationView, DataSetFileActionView
from schemas.websockets.consumer_is_csv_ready import IsCSVReadyConsumer

urlpatterns = [
    path('', SchemaView.as_view(), name='index'),
    path('schemas/', SchemaCreationView.as_view(), name="create_schema"),
    path('schemas/<int:schema_id>/delete', SchemaDeletionView.as_view(), name='delete_schema'),
    path('schemas/<int:schema_id>/edit', SchemaEditView.as_view(), name="edit_schema"),
    path('schemas/<int:schema_id>/data-sets/', DataSetCreationView.as_view(), name='create_data_set'),
    path('media/generated_csv/<int:schema_id>/data-sets/<str:uuid>', DataSetFileActionView.as_view(), name='file_data_set'),
    path('ws/', IsCSVReadyConsumer.as_asgi())
]

from django.contrib import admin
from django.urls import path, include
from schemas import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ws/', IsCSVReadyConsumer.as_asgi())
]

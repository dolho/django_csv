"""csv_creator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from schemas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('schemas.urls')),
    # path('', views.index, name='index'),
    # path('accounts/', include('django.contrib.auth.urls'), name='login'),
    path('accounts/login/', views.login_view, name='login'),
    # path('schemas/', views.create_schema, name='create_schema'),
    # path('schemas/<int:schema_id>/data-sets/', views.create_data_set, name='create_data_set'),
    # path('schemas/<int:schema_id>/data-sets/<str:timestamp>', views.load_data_set, name='load_data_set'),
    # path('ws/', IsCSVReadyConsumer.as_asgi())
]

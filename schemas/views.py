from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from schemas.models import Schema
from schemas.schema_service import SchemaService
from schemas.fake_csv_generator.fake_csv_generator import generate_csv
from django.views import View
import itertools
import functools
import json
from django.shortcuts import get_object_or_404
import os
from datetime import datetime
from pathlib import Path
from django.http import FileResponse
import time
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.



class SchemaView(LoginRequiredMixin, View):

    def get(self, request):
        schemas = Schema.objects.filter(author_id=request.user)
        return render(request, "data_schemas.html",
                      {'iterator': functools.partial(next, itertools.count()),
                       'schemas': schemas})


class SchemaCreationView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "schema_creation.html")

    def post(self, request):
        try:
            data = json.loads(request.body)
            new_schema = Schema.objects.create(author_id=request.user, name=data['schemaName'], separator=data['separatorColumn'],
                                  stringCharacter=data['stringCharachter'], columns=data['columns'])
            new_schema.save()
            return HttpResponseRedirect(reverse('index'))
        except KeyError:
            return HttpResponseBadRequest()


class DataSetCreationView(LoginRequiredMixin, View):

    def get(self, request, schema_id):
        schema = get_object_or_404(Schema, pk=schema_id)
        schema_data_sets_directory = SCHEMA_SERVICE.get_schema_folder_path(request.user.id, schema_id)
        result = []
        try:
            for filename in os.scandir(schema_data_sets_directory):
                if filename.is_file():
                    name_without_extension = Path(filename).stem
                    result.append(
                        (datetime.fromtimestamp(float(name_without_extension)).date(), name_without_extension))
        except FileNotFoundError:
            pass
        return render(request, "data_sets.html",
                      {'iterator': functools.partial(next, itertools.count()),
                       'data_sets': result,
                       'schema_id': schema_id
                       })

    def post(self, request, schema_id):
        schema = get_object_or_404(Schema, pk=schema_id)
        try:
            amount_of_rows = int(request.POST['rowsAmount'])
        except ValueError:
            return HttpResponseBadRequest()
        time_now = time.time()
        generate_csv.delay(schema.columns, time_now, request.user.id, schema_id, amount_of_rows)
        return HttpResponseRedirect(reverse("create_data_set", kwargs={'schema_id': schema_id}))

class DataSetLoadView(LoginRequiredMixin, View):

    def get(self, request, schema_id, timestamp):
        path = SCHEMA_SERVICE.get_schema_folder_path(request.user.id, schema_id)
        csv_data_set = open(os.path.join(path, timestamp + '.csv'), 'rb')
        response = FileResponse(csv_data_set)
        return response

# @login_required
# def index(request):
#     schemas = Schema.objects.filter(author_id=request.user)
#     return render(request, "data_schemas.html", {'iterator': functools.partial(next, itertools.count()),
#                                                  'schemas': schemas})


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'registration/login.html', {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "registration/login.html", {"login_url": reverse('login')})


# @login_required
# def create_schema(request):
#     if request.method == "GET":
#         return render(request, "schema_creation.html")
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             new_schema = Schema.objects.create(author_id=request.user, name=data['schemaName'], separator=data['separatorColumn'],
#                                   stringCharacter=data['stringCharachter'], columns=data['columns'])
#             new_schema.save()
#             return HttpResponseRedirect(reverse('index'))
#         except KeyError:
#             return HttpResponseBadRequest()


# FAKER = Faker()
# SCHEMA_SERVICE = SchemaService(IntegerColumn(0, 1, name='initial', faker=FAKER,
#                                next=JobColumn(name='initial', faker=FAKER,
#                                next=FullNameColumn(name='initial', faker=FAKER))))

# FAKE_CSV_GENERATOR = FakeCSVGenerator()
SCHEMA_SERVICE = SchemaService()

# @login_required
# def create_data_set(request, schema_id):
#     schema = get_object_or_404(Schema, pk=schema_id)
#     if request.method == "GET":
#         schema_data_sets_directory = SCHEMA_SERVICE.get_schema_folder_path(request.user.id, schema_id)
#         result = []
#         try:
#             for filename in os.scandir(schema_data_sets_directory):
#                 if filename.is_file():
#                     name_without_extension = Path(filename).stem
#                     result.append((datetime.fromtimestamp(float(name_without_extension)).date(), name_without_extension))
#         except FileNotFoundError:
#             pass
#         return render(request, "data_sets.html",
#                       {'iterator': functools.partial(next, itertools.count()),
#                        'data_sets': result,
#                        'schema_id': schema_id
#                        })
#     if request.method == "POST":
#         try:
#             amount_of_rows = int(request.POST['rowsAmount'])
#         except ValueError:
#             return HttpResponseBadRequest()
#         time_now = time.time()
#         generate_csv.delay(schema.columns, time_now, request.user.id, schema_id, amount_of_rows)
#         return HttpResponseRedirect(reverse("create_data_set", kwargs={'schema_id': schema_id}))


# @login_required
# def load_data_set(request, schema_id, timestamp):
#     path = SCHEMA_SERVICE.get_schema_folder_path(request.user.id, schema_id)
#     csv_data_set = open(os.path.join(path, timestamp + '.csv'), 'rb')
#     response = FileResponse(csv_data_set)
#     return response
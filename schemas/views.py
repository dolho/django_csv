from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from schemas.models import Schema
from schemas.schema_service import SchemaService
from schemas.data_set_service import DataSetService
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
        result = DATA_SET_SERVICE.get_data_sets(schema_data_sets_directory)
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

    def get(self, request, schema_id, uuid):
        path = SCHEMA_SERVICE.get_schema_folder_path(request.user.id, schema_id)
        with open(DATA_SET_SERVICE.path_to_file(path, uuid), 'rb') as f:
            response = FileResponse(f)
        return response


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


SCHEMA_SERVICE = SchemaService()
DATA_SET_SERVICE = DataSetService()


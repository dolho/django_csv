from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, reverse
from schemas.models import Schema, DataSet
from schemas.schema_service import SchemaService
from schemas.data_set_service import DataSetService
from schemas.fake_csv_generator.fake_csv_generator import generate_csv
from django.views import View
import itertools
import functools
import json
from django.shortcuts import get_object_or_404
import os
from cloudinary.uploader import destroy
import time
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
# Create your views here.


SCHEMA_SERVICE = SchemaService()
DATA_SET_SERVICE = DataSetService()

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
            new_schema = Schema(author_id=request.user, name=data['schemaName'],
                                               separator=data['separatorColumn'],
                                               stringCharacter=data['stringCharachter'], columns=data['columns'])
            if not SCHEMA_SERVICE.is_user_allowed_to_create_schema(request.user, len(data['columns'])):
                return JsonResponse({"error": "You can't create schema. Maybe you already "
                                    "reached limit of schemas or you trying to add "
                                    "more than 10 columns. "}, status=403)
                # TODO Change to changeable error response
            new_schema.save()
            return HttpResponseRedirect(reverse('index'))
        except KeyError:
            return HttpResponseBadRequest()


class SchemaDeletionView(LoginRequiredMixin, View):

    def post(self, request, schema_id):
        schema = get_object_or_404(Schema, pk=schema_id)
        if schema.author_id != request.user:
            return HttpResponseForbidden()
        schema.delete()
        return HttpResponseRedirect(reverse('index'))


class SchemaEditView(LoginRequiredMixin, View):

    def get(self, request, schema_id):
        schema = get_object_or_404(Schema, pk=schema_id)
        if schema.author_id != request.user:
            return HttpResponseForbidden()
        return render(request, "schema_edit.html", {"schema": schema,
                                                    "current_order": schema.columns[-1]['columnOrder']})

    def post(self, request, schema_id):
        schema = get_object_or_404(Schema, pk=schema_id)
        if schema.author_id != request.user:
            return HttpResponseForbidden()
        try:
            data = json.loads(request.body)
            is_user_allowed_to_edit = SCHEMA_SERVICE.is_user_allowed_to_edit_schema(request.user, len(data['columns']))
            if not is_user_allowed_to_edit:
                return JsonResponse({"error": "Schema can't have more than 10 rows"},
                                    status=403)

            Schema.objects.filter(id=schema_id).update(author_id=request.user, name=data['schemaName'], separator=data['separatorColumn'],
                                  stringCharacter=data['stringCharachter'], columns=data['columns'])
            return HttpResponseRedirect(reverse('index'))
        except KeyError:
            return HttpResponseBadRequest()


class DataSetCreationView(LoginRequiredMixin, View):

    def get(self, request, schema_id: int):
        schema = get_object_or_404(Schema, pk=schema_id)
        schema_data_sets_directory = SCHEMA_SERVICE.get_schema_folder_path(request.user.id, schema_id)
        result = DATA_SET_SERVICE.get_data_sets(schema_id) # schema_data_sets_directory
        return render(request, "data_sets.html",
                      {'iterator': functools.partial(next, itertools.count()),
                       'data_sets': result,
                       'schema_id': schema_id
                       })

    def post(self, request, schema_id: int):
        schema = get_object_or_404(Schema, pk=schema_id)
        try:
            amount_of_rows = int(request.POST['rowsAmount'])
            if amount_of_rows < 0:
                return HttpResponseBadRequest("Amount of rows can't be less than 0")
        except ValueError:
            return HttpResponseBadRequest("No rowsAmount given")
        if not DATA_SET_SERVICE.is_user_allowed_to_create_dataset(request.user, schema, amount_of_rows):
            return render(request, 'error.html', {'schema_id': schema_id,
                                                  'errors': ["You can't have more than 2 data sets for "
                                                  "each schema and make dataset longer than "
                                                  "500 000 rows "]})
        # TODO Change to changeable error response
        generate_csv.delay(schema.columns, request.user.id, schema_id, amount_of_rows)
        return HttpResponseRedirect(reverse("create_data_set", kwargs={'schema_id': schema_id}))


class DataSetFileActionView(LoginRequiredMixin, View):

    # def get(self, request, schema_id, uuid):
    #     path = SCHEMA_SERVICE.get_schema_folder_path(request.user.id, schema_id)
    #     with open(DATA_SET_SERVICE.path_to_file(path, uuid), 'rb') as f:
    #         print(f)
    #         response = FileResponse(f)
    #     return response

    def post(self, request, schema_id, uuid):
        schema = get_object_or_404(Schema, pk=schema_id)
        if schema.author_id != request.user:
            return HttpResponseForbidden()
        dataset = DataSet.objects.get(pk=uuid)
        public_id = dataset.path_to_file.rsplit('/', 1)[-1] #.rsplit('.')[0]
        print(public_id)
        cloudinary_response = destroy(public_id, resource_type='raw')
        if cloudinary_response["result"] == "ok":
            dataset.delete()
        else:
            print(cloudinary_response)
        return HttpResponseRedirect(reverse('create_data_set', kwargs={'schema_id': schema_id}))




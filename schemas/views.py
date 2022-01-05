from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import path, include
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index(request):
    return render(request, "data_schemas.html")
    # return HttpResponse("Hello, world. You're at the polls index.")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            print(request.GET)
            print(request.POST)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'registration/login.html', {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "registration/login.html", {"login_url": reverse('login')})


@login_required
def create_schema(request):
    if request.method == "GET":
        return render(request, "schema_creation.html")
    if request.method == "POST":
        print(request.POST)

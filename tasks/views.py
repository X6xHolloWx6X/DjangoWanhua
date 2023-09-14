from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # acá es donde se captura de los inputs y los almacena en las variables, para ser salvado
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(
                    # si el usuario ya existe, se le devuelve el formulario con un mensaje de error
                    request,
                    "signup.html",
                    {"form": UserCreationForm(), "error": "Usuario ya existe"},
                )

        return render(
            # si es muy mogolico y no pone bien la contraseña, se le devuelve el formulario con un mensaje de error
            request,
            "signup.html",
            {"form": UserCreationForm(), "error": "Contraseña no coincide"},
        )


def tasks(request):
    return render(request, "tasks.html")


def cerrar_sesion(request):
    logout(request)
    return redirect("home")


def login_entrar(request):
    if request.method == 'GET':
        return render(request, "login.html", {"form": AuthenticationForm})
    else:
        user =authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "login.html",
                {"form": AuthenticationForm, "error": "Usuario y/o contraseña incorrectos"},
            )
        else:
            login(request, user)
            return redirect("tasks")
        
        return render(request, "login.html", {"form": AuthenticationForm})

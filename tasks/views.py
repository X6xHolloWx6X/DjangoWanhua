from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse

from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Propiedades
from .forms import ClienteForm, PropiedadesForm


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
        

def cliente_list(request):
    clientes = Cliente.objects.all()
    form = None
    return render(request, 'clientes.html', {'clientes': clientes, 'form': form})

def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('cliente_list'))
    else:
        form = ClienteForm()
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'form': form, 'clientes': clientes})

def cliente_update(request, dni):
    cliente = Cliente.objects.get(dni=dni)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)  # Asegúrate de pasar 'instance=cliente'
        if form.is_valid():
            form.save()
            return redirect(reverse('cliente_list'))
    else:
        form = ClienteForm(instance=cliente)
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'form': form, 'clientes': clientes})


def cliente_delete(request, dni):
    cliente = Cliente.objects.get(dni=dni)
    cliente.delete()
    return redirect(reverse('cliente_list'))

def propiedades_list(request, dni_cliente):
    cliente = get_object_or_404(Cliente, dni=dni_cliente)
    if request.method == 'POST':
        form = PropiedadesForm(request.POST)
        if form.is_valid():
            propiedad = form.save(commit=False)
            propiedad.cliente = cliente
            propiedad.save()
            return redirect('propiedades_list_by_dni', dni_cliente=dni_cliente)
    else:
        form = PropiedadesForm()

    propiedades = Propiedades.objects.filter(cliente=cliente)
    return render(request, 'propiedades.html', {'propiedades': propiedades, 'form': form, 'cliente': cliente})


def propiedades_edit(request, id):
    propiedad = get_object_or_404(Propiedades, ID_prop=id)
    if request.method == 'POST':
        form = PropiedadesForm(request.POST, instance=propiedad)
        if form.is_valid():
            form.save()
            return redirect('propiedades_list_by_dni', dni_cliente=propiedad.cliente.dni)
    else:
        form = PropiedadesForm(instance=propiedad)
    return render(request, 'propiedades.html', {'form': form, 'cliente': propiedad.cliente, 'editing': True})


def propiedades_delete(request, id):
    propiedad = get_object_or_404(Propiedades, ID_prop=id)
    if request.method == 'POST':
        propiedad.delete()
        return redirect('propiedades_list_by_dni', dni_cliente=propiedad.cliente.dni)
    return render(request, 'propiedades.html', {'propiedad_to_delete': propiedad, 'cliente': propiedad.cliente})

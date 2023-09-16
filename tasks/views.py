from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, JsonResponse
from .models import Cliente
from .forms import ClienteForm
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
        

def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Cliente creado correctamente'})
        else:
            return JsonResponse({'error': 'Error en el formulario'}, status=400)
    return JsonResponse({'error': 'Método no válido'}, status=400)

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Cliente actualizado correctamente'})
        else:
            return JsonResponse({'error': 'Error en el formulario'}, status=400)
    return JsonResponse({'error': 'Método no válido'}, status=400)

def eliminar_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.get(pk=cliente_id)
        cliente.delete()
        return JsonResponse({'message': 'Cliente eliminado correctamente'})
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)
    
def obtener_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id_cliente=cliente_id)
    data = {
        'id_cliente': cliente.id_cliente,
        'nombre': cliente.nombre,
        'apellido': cliente.apellido,
        'dni': cliente.dni,
        'fecha_nacimiento': cliente.fecha_nacimiento,
        'tipo_cliente': cliente.tipo_cliente,
        # Otros campos si es necesario
    }
    return JsonResponse({'cliente': data})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from .models import Cliente, Propiedades, Contrato
from .forms import ClienteForm, PropiedadesForm, ContratoForm
import os
from django.conf import settings


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
    search_query = request.GET.get('search')
    clientes_list = Cliente.objects.all()

    if search_query:
        clientes_list = clientes_list.filter(
            Q(dni__icontains=search_query) |
            Q(nombre_cliente__icontains=search_query) |
            Q(tel_cliente__icontains=search_query) |
            Q(email_cliente__icontains=search_query) |
            Q(direccion_cliente__icontains=search_query)
        )

    paginator = Paginator(clientes_list, 2)
    page = request.GET.get('page')
    clientes = paginator.get_page(page)

    form = None
    return render(request, 'clientes.html', {'clientes': clientes, 'form': form})

def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
    else:
        form = ClienteForm()
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'form': form, 'clientes': clientes})

def cliente_update(request, dni):
    cliente = Cliente.objects.get(dni=dni)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
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
        form = PropiedadesForm(request.POST, request.FILES)  # Agregar request.FILES
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
        form = PropiedadesForm(request.POST, request.FILES, instance=propiedad)
        if form.is_valid():
            # Lógica para eliminar las imágenes antiguas si se actualizan
            propiedad_actual = Propiedades.objects.get(ID_prop=id)
            for field_name in ['foto1', 'foto2', 'foto3']:
                field = getattr(propiedad_actual, field_name)
                new_field = form.cleaned_data[field_name]
                if field and new_field and field != new_field and field.name != 'propiedades/fotos/default.jpg':
                    file_path = os.path.join(settings.MEDIA_ROOT, field.name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

            form.save()
            return redirect('propiedades_list_by_dni', dni_cliente=propiedad.cliente.dni)
    else:
        form = PropiedadesForm(instance=propiedad)
    return render(request, 'propiedades.html', {'form': form, 'cliente': propiedad.cliente, 'editing': True})

def propiedades_delete(request, id):
    propiedad = get_object_or_404(Propiedades, ID_prop=id)
    if request.method == 'POST':
        # Lógica para eliminar imágenes asociadas, excepto default.jpg
        for field in [propiedad.foto1, propiedad.foto2, propiedad.foto3]:
            if field and field.name != 'propiedades/fotos/default.jpg':
                file_path = os.path.join(settings.MEDIA_ROOT, field.name)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        propiedad.delete()
        return redirect('propiedades_list_by_dni', dni_cliente=propiedad.cliente.dni)
    return render(request, 'propiedades.html', {'propiedad_to_delete': propiedad, 'cliente': propiedad.cliente})

def listar_contratos_cliente(request, dni_cliente):
    # Aquí puedes implementar la lógica para obtener los contratos del cliente con el dni proporcionado
    contratos = Contrato.objects.filter(cliente__dni=dni_cliente)

    # Luego, renderiza una plantilla con los contratos y cualquier otra información que desees mostrar
    return render(request, 'contratos.html', {'contratos': contratos, 'dni_cliente': dni_cliente})

def listar_contratos(request):
    contratos = Contrato.objects.all()
    for contrato in contratos:
        contrato.fecha_inicio = contrato.fecha_inicio.strftime('%d/%m/%Y')
        contrato.fecha_fin = contrato.fecha_fin.strftime('%d/%m/%Y')
    return render(request, 'contratos.html', {'contratos': contratos})


def crear_contrato(request, dni_cliente, propiedad_id):
    cliente = get_object_or_404(Cliente, dni=dni_cliente)
    propiedad = get_object_or_404(Propiedades, ID_prop=propiedad_id)

    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            nuevo_contrato = form.save(commit=False)
            nuevo_contrato.cliente = cliente
            nuevo_contrato.propiedades = propiedad
            nuevo_contrato.save()
            return redirect('listar_contratos')
    else:
        # Pasa los valores de cliente y propiedad en el contexto del formulario
        form = ContratoForm(initial={'cliente': cliente, 'propiedades': propiedad})

    # Agrega 'is_creating_new' al contexto
    context = {
        'form': form, 
        'cliente': cliente, 
        'propiedad': propiedad,
        'is_creating_new': True  # Añade esta línea
    }
    return render(request, 'contratos.html', context)


def actualizar_contrato(request, id_contrato):
    contrato = get_object_or_404(Contrato, id_contrato=id_contrato)
    if request.method == 'POST':
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            form.save()
            return redirect('listar_contratos')
    else:
        form = ContratoForm(instance=contrato)

    return render(request, 'contratos.html', {'form': form, 'contrato': contrato})

def eliminar_contrato(request, id_contrato):
    contrato = get_object_or_404(Contrato, id_contrato=id_contrato)
    if request.method == 'POST':
        contrato.delete()
        return redirect('listar_contratos')

    return render(request, 'confirmar_eliminacion.html', {'contrato': contrato})

def eliminar_contrato(request, id_contrato):
    contrato = get_object_or_404(Contrato, id_contrato=id_contrato)
    if request.method == 'POST':
        contrato.delete()
        return redirect('listar_contratos')

    return render(request, 'confirmar_eliminacion.html', {'contrato': contrato})
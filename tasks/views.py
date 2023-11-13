from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from .models import Cliente, Propiedades, Contrato
from .forms import ClienteForm, PropiedadesForm, ContratoForm
import os
from datetime import datetime
from django.conf import settings
import textwrap

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


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


def propiedades_clientes_todas(request):
    # Obtener el término de búsqueda del query string
    search_query = request.GET.get('search', '')

    # Filtrar propiedades según la búsqueda
    if search_query:
        propiedades = Propiedades.objects.select_related('cliente').filter(
            Q(direccion__icontains=search_query) | 
            Q(cliente__nombre_cliente__icontains=search_query) | 
            Q(cliente__dni__icontains=search_query)
        )
    else:
        propiedades = Propiedades.objects.select_related('cliente').all()
    for propiedad in propiedades:
        # Crear una lista de imágenes
        propiedad.lista_imagenes = [propiedad.foto1, propiedad.foto2, propiedad.foto3]

    # Paginación
    paginator = Paginator(propiedades, 3)  # 10 propiedades por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'propiedades_clientes.html', {'propiedades': page_obj})






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
    search_query = request.GET.get('search')
    contratos = Contrato.objects.filter(cliente__dni=dni_cliente)

    if search_query:
        contratos = contratos.filter(
            Q(id_contrato__icontains=search_query) |
            Q(cliente__nombre_cliente__icontains=search_query) |
            Q(cliente__dni__icontains=search_query) |
            Q(propiedades__ID_prop__icontains=search_query) |
            Q(propiedades__direccion__icontains=search_query) |
            Q(fecha_inicio__icontains=search_query) |
            Q(fecha_fin__icontains=search_query) |
            Q(descripcion__icontains=search_query)
        )

    paginator = Paginator(contratos, 2)
    page = request.GET.get('page')

    try:
        contratos_paginated = paginator.page(page)
    except PageNotAnInteger:
        contratos_paginated = paginator.page(1)
    except EmptyPage:
        contratos_paginated = paginator.page(paginator.num_pages)

    dni_cliente = dni_cliente  # Puedes mantenerlo si lo necesitas
    return render(request, 'contratos.html', {'contratos': contratos_paginated, 'dni_cliente': dni_cliente})

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


def actualizar_contrato(request, id_contrato, dni_cliente):
    contrato = get_object_or_404(Contrato, id_contrato=id_contrato)
    if request.method == 'POST':
        form = ContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            form.save()
            return redirect('listar_contratos_cliente', dni_cliente=dni_cliente)
    else:
        form = ContratoForm(instance=contrato)

    return render(request, 'contratos.html', {'form': form, 'contrato': contrato, 'dni_cliente': dni_cliente})

def eliminar_contrato(request, id_contrato, dni_cliente):
    contrato = get_object_or_404(Contrato, id_contrato=id_contrato)
    if request.method == 'POST':
        contrato.delete()
        return redirect('listar_contratos_cliente', dni_cliente=dni_cliente)

    return render(request, 'confirmar_eliminacion.html', {'contrato': contrato, 'dni_cliente': dni_cliente})


def generar_contrato_pdf(request, id_contrato):
    contrato = get_object_or_404(Contrato, id_contrato=id_contrato)
    cliente = contrato.cliente
    propiedad = contrato.propiedades

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contrato_{contrato.id_contrato}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Times-Bold", 14)

    # Encabezado del contrato
    p.drawString(50, 800, "Contrato de Administración de Propiedad")
    p.setFont("Times-Roman", 12)
    p.drawString(50, 780, f"El presente contrato se celebra el día {datetime.now().strftime('%d/%m/%Y')} entre Inmobiliaria Wanhua y:")
    p.drawString(50, 765, f"Propietario: {cliente.nombre_cliente} (DNI: {cliente.dni})")

    # Información de la propiedad
    p.drawString(50, 750, f"Propiedad: {propiedad.direccion} (Área: {propiedad.area_total}m², Habitaciones: {propiedad.nro_habitaciones})")
    p.drawString(50, 735, f"Valor de Alquiler Estimado: ${propiedad.precio_alq}")

    # Cláusulas del contrato
    p.setFont("Times-Roman", 11)
    clausulas = [
        f"CLÁUSULA PRIMERA: Objeto del Contrato - El presente contrato tiene por objeto la administración de la propiedad indicada, por parte de Inmobiliaria Wanhua, quien actuará como administrador de la misma.",
        f"CLÁUSULA SEGUNDA: Duración - Este contrato tiene una duración de un año, iniciando el {contrato.fecha_inicio.strftime('%d/%m/%Y')} y concluyendo el {contrato.fecha_fin.strftime('%d/%m/%Y')}, con opción de renovación previo acuerdo de ambas partes."
        # Agrega más cláusulas según sea necesario
    ]

    y_position = 720
    for clausula in clausulas:
        wrapped_text = textwrap.fill(clausula, 100)
        for line in wrapped_text.split('\n'):
            p.drawString(50, y_position, line)
            y_position -= 15
        y_position -= 10  # Espacio adicional entre cláusulas

    # Espacio para las firmas
    p.setFont("Times-Roman", 12)
    p.drawString(50, y_position - 40, "Firma del Propietario: ___________________________")
    p.drawString(50, y_position - 60, "Firma del Representante de Inmobiliaria Wanhua: ___________________________")
    p.drawString(50, y_position - 80, "Fecha de Firma: ___________________________")

    p.showPage()
    p.save()
    return response


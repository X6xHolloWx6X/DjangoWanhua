from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path("signup/", views.signup, name="signup"),   
    path("tasks/", views.tasks, name="tasks"),
    path("salir/", views.cerrar_sesion, name="cerrar_sesion"),
    path("login/", views.login_entrar, name="entrar_sesion"),
    path('clientes/', views.gestion_clientes, name='lista_clientes'),
    path('clientes/crear/', views.gestion_clientes, {'accion': 'crear'}, name='crear_cliente'),
    path('clientes/editar/<str:dni>/', views.gestion_clientes, {'accion': 'editar'}, name='editar_cliente'),
    path('clientes/eliminar/<str:dni>/', views.gestion_clientes, {'accion': 'eliminar'}, name='eliminar_cliente'),
]

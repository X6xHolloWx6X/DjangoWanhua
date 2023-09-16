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
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('clientes/obtener/<int:cliente_id>/', views.obtener_cliente, name='obtener_cliente'),
]

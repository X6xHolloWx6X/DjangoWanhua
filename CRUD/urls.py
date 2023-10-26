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
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('cliente/<str:dni>/', views.detalle_cliente, name='detalle_cliente'),
    path('cliente/nuevo/', views.crear_cliente, name='crear_cliente'),      
    path('cliente/editar/<str:dni>/', views.editar_cliente, name='editar_cliente'),
    path('cliente/eliminar/<str:dni>/', views.eliminar_cliente, name='eliminar_cliente'),

]

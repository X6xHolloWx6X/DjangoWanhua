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
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('cliente/create/', views.cliente_create, name='cliente_create'),
    path('cliente/update/<str:dni>/', views.cliente_update, name='cliente_update'),
    path('cliente/delete/<str:dni>/', views.cliente_delete, name='cliente_delete'),
    path('propiedades/', views.propiedades_list, name='propiedades_list'),
    path('propiedades/<str:dni_cliente>/', views.propiedades_list, name='propiedades_list_by_dni'),
    path('propiedades/<int:id>/edit/', views.propiedades_edit, name='propiedades_edit'),
    path('propiedades/<int:id>/delete/', views.propiedades_delete, name='propiedades_delete'),

]

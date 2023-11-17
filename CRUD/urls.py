from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static
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
    # En tu urls.py
path('propiedades-clientes/', views.propiedades_clientes_todas, name='propiedades_clientes_todas'),

    path('contratos/', views.listar_contratos, name='listar_contratos'),
    path('contratos/cliente/<str:dni_cliente>/', views.listar_contratos, name='listar_contratos_cliente'),
    path('contratos/crear/<str:dni_cliente>/<int:propiedad_id>/', views.crear_contrato, name='crear_contrato'),
    path('contratos/actualizar/<int:id_contrato>/<str:dni_cliente>/', views.actualizar_contrato, name='actualizar_contrato'),
    path('contratos/eliminar/<int:id_contrato>/<str:dni_cliente>/', views.eliminar_contrato, name='eliminar_contrato'),

    path('contratos/generar_pdf/<int:id_contrato>/', views.generar_contrato_pdf, name='generar_contrato_pdf'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
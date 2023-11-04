from django import forms
from .models import Cliente, Propiedades

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['dni', 'nombre_cliente', 'tel_cliente', 'email_cliente', 'direccion_cliente']

class PropiedadesForm(forms.ModelForm):
    class Meta:
        model = Propiedades
        fields = ['cliente', 'area_total', 'nro_habitaciones', 'precio_alq', 'descripcion']
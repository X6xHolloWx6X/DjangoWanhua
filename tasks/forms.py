from django import forms
from .models import Cliente, TpoCliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class TpoClienteForm(forms.ModelForm):
    class Meta:
        model = TpoCliente
        fields = '__all__'
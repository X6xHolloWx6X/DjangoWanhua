from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente, Propiedades, Contrato, Convenio
from datetime import date
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['dni', 'nombre_cliente', 'tel_cliente', 'email_cliente', 'direccion_cliente']

class PropiedadesForm(forms.ModelForm):
    class Meta:
        model = Propiedades
        fields = ['cliente', 'area_total', 'nro_habitaciones', 'precio_alq', 'descripcion', 'direccion', 'foto1', 'foto2', 'foto3']
        

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['cliente', 'propiedades', 'fecha_inicio', 'fecha_fin', 'descripcion']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }  
        labels = {
             'cliente': 'DNI Cliente',
            'propiedades': 'Propiedad ID'
        }

    def __init__(self, *args, **kwargs):
        super(ContratoForm, self).__init__(*args, **kwargs)
         
        if self.instance and self.instance.pk:
            self.fields['fecha_inicio'].initial = self.instance.fecha_inicio
            self.fields['fecha_fin'].initial = self.instance.fecha_fin


        # Establece automáticamente el ID de propiedad y el DNI del cliente si están disponibles en la solicitud
        if 'initial' in kwargs:
            initial_data = kwargs['initial']
            propiedades_id = initial_data.get('propiedades_id')
            cliente_dni = initial_data.get('cliente_dni')

            if propiedades_id:
                self.fields['propiedades'].initial = propiedades_id

            if cliente_dni:
                self.fields['cliente'].initial = cliente_dni

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get("fecha_inicio")
        fecha_fin = cleaned_data.get("fecha_fin")
        propiedades = cleaned_data.get("propiedades")

        # Comprobación de que la fecha de inicio no sea posterior a la fecha de fin
        if fecha_inicio and fecha_fin:
            if fecha_inicio > fecha_fin:
                raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")

            # Verificar si hay solapamiento de fechas
            contratos_existentes = Contrato.objects.filter(propiedades=propiedades)
            
            if self.instance and self.instance.pk:
                contratos_existentes = contratos_existentes.exclude(pk=self.instance.pk)

            for contrato in contratos_existentes:
                if (fecha_inicio <= contrato.fecha_fin and fecha_fin >= contrato.fecha_inicio):
                    raise ValidationError("Las fechas del contrato se solapan con otro contrato existente para esta propiedad.")

        return cleaned_data

class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Convenio
        fields = ['id_contrato', 'fecha_inicio', 'fecha_fin', 'descripcion']
        widgets = {
            'fecha_inicio': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}),
            'fecha_fin': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker'}),
            # Si decides ocultar el campo id_contrato, puedes usar forms.HiddenInput()
            'id_contrato': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        contrato_id = kwargs.pop('contrato_id', None)
        super(ConvenioForm, self).__init__(*args, **kwargs)
        if contrato_id:
            self.fields['id_contrato'].initial = contrato_id
            # Si no quieres que el usuario cambie este campo, puedes deshabilitarlo
            self.fields['id_contrato'].disabled = True
    
    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        # Asegúrate de que la fecha de inicio no sea una fecha pasada
        if fecha_inicio < date.today():
            raise ValidationError('La fecha de inicio no puede ser en el pasado.')
        return fecha_inicio

    def clean_fecha_fin(self):
        fecha_fin = self.cleaned_data.get('fecha_fin')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        # Asegúrate de que la fecha de fin sea posterior a la fecha de inicio
        if fecha_fin and fecha_inicio and fecha_fin < fecha_inicio:
            raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')
        return fecha_fin
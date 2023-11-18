from django.db import models
from datetime import datetime

class Cliente(models.Model):
    dni = models.CharField(max_length=50, primary_key=True)
    nombre_cliente = models.CharField(max_length=200)
    tel_cliente = models.CharField(max_length=50)
    email_cliente = models.EmailField()
    direccion_cliente = models.CharField(max_length=300)

class Propiedades(models.Model):
    ID_prop = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    area_total = models.FloatField()
    nro_habitaciones = models.IntegerField()
    precio_alq = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    
    direccion = models.CharField(max_length=255, null=True, blank=True)
    foto1 = models.ImageField(upload_to='propiedades/fotos/', null=True, blank=True, default='propiedades/fotos/default.jpg')
    foto2 = models.ImageField(upload_to='propiedades/fotos/', null=True, blank=True, default='propiedades/fotos/default.jpg')
    foto3 = models.ImageField(upload_to='propiedades/fotos/', null=True, blank=True, default='propiedades/fotos/default.jpg')

class Contrato(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    propiedades = models.ForeignKey(Propiedades, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField()

    def fecha_inicio_formatted(self):
        return self.fecha_inicio.strftime('%d/%m/%Y')

    def fecha_fin_formatted(self):
        return self.fecha_fin.strftime('%d/%m/%Y')

    def save(self, *args, **kwargs):
        # Parsea las fechas en formato 'dd/mm/yyyy' a 'yyyy-mm-dd'
        if isinstance(self.fecha_inicio, str) and '/' in self.fecha_inicio:
            day, month, year = self.fecha_inicio.split('/')
            self.fecha_inicio = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()
        if isinstance(self.fecha_fin, str) and '/' in self.fecha_fin:
            day, month, year = self.fecha_fin.split('/')
            self.fecha_fin = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()
        
        super(Contrato, self).save(*args, **kwargs)

class Convenio(models.Model):
    ID_convenio = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField()

    def fecha_inicio_formatted(self):
        return self.fecha_inicio.strftime('%d/%m/%Y')

    def fecha_fin_formatted(self):
        return self.fecha_fin.strftime('%d/%m/%Y')

    def save(self, *args, **kwargs):
        # Parsea las fechas en formato 'dd/mm/yyyy' a 'yyyy-mm-dd'
        if isinstance(self.fecha_inicio, str) and '/' in self.fecha_inicio:
            day, month, year = self.fecha_inicio.split('/')
            self.fecha_inicio = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()
        if isinstance(self.fecha_fin, str) and '/' in self.fecha_fin:
            day, month, year = self.fecha_fin.split('/')
            self.fecha_fin = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()

        super(Convenio, self).save(*args, **kwargs)
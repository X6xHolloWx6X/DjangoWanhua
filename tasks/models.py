from django.db import models

class Cliente(models.Model):
        dni = models.CharField(max_length=50, primary_key=True)
        nombre_cliente = models.CharField(max_length=200)
        tel_cliente = models.CharField(max_length=50)
        email_cliente = models.EmailField()
        direccion_cliente = models.CharField(max_length=300)
        # ... y cualquier otro campo o método que hayas definido

class Propiedades(models.Model):
    ID_prop = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    area_total = models.FloatField()
    nro_habitaciones = models.IntegerField()
    precio_alq = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    
    # Agregando dirección con la posibilidad de ser nulo y sin valor por defecto
    direccion = models.CharField(max_length=255, null=True, blank=True)

    # Agregando campos para las fotos con la posibilidad de ser nulos
    foto1 = models.ImageField(upload_to='propiedades/fotos/', null=True, blank=True, default='propiedades/fotos/default.jpg')
    foto2 = models.ImageField(upload_to='propiedades/fotos/', null=True, blank=True, default='propiedades/fotos/default.jpg')
    foto3 = models.ImageField(upload_to='propiedades/fotos/', null=True, blank=True, default='propiedades/fotos/default.jpg')

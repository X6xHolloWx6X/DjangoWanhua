from django.db import models

class Cliente(models.Model):
    dni = models.CharField(max_length=50, primary_key=True)
    nombre_cliente = models.CharField(max_length=200)
    tel_cliente = models.CharField(max_length=50)
    email_cliente = models.EmailField()
    direccion_cliente = models.CharField(max_length=300)
    # ... y cualquier otro campo o método que hayas definido

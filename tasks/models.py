from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=10)
    tipo_cliente = models.CharField(max_length=20, choices=[('propietario', 'Propietario'), ('inquilino', 'Inquilino')])

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

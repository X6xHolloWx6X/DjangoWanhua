from django.db import models

class Cliente(models.Model):
    TIPOS_CLIENTE = (
        ('inquilino', 'Inquilino'),
        ('propietario', 'Propietario'),
    )

    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    tipo_cliente = models.CharField(max_length=20, choices=TIPOS_CLIENTE)

    # Permitir fecha de nacimiento nula
    fecha_nacimiento = models.DateField(null="YYYY-MM-DD", blank=True)

    # Si el cliente es un inquilino, se requieren detalles del garante
    garante_nombre = models.CharField(max_length=100, blank=True, null=True)
    garante_apellido = models.CharField(max_length=100, blank=True, null=True)
    garante_dni = models.CharField(max_length=20, blank=True, null=True)

    # Agregar campos de dirección para inquilino y garantes
    direccion_inquilino = models.CharField(max_length=255, blank=True, null=True)
    direccion_garante = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
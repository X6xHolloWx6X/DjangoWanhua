from django.db import models

class TpoCliente(models.Model):
    id_tpo_cliente = models.AutoField(primary_key=True)  # Removido null=True
    descripcion = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.descripcion

class Garante(models.Model):
    dni_garante = models.CharField(max_length=8, primary_key=True, null=False)
    nombre = models.CharField(max_length=255, null=True, blank=True)
    apellido = models.CharField(max_length=255, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Cliente(models.Model):
    dni = models.CharField(max_length=8, primary_key=True, null=False)
    nombre_cliente = models.CharField(max_length=255, null=True, blank=False)
    tel_cliente = models.CharField(max_length=15, null=True, blank=False)
    email_cliente = models.EmailField(null=True, blank=True)  # Cambiado blank a True
    direccion_cliente = models.TextField(null=True, blank=True)  # Cambiado blank a True
    id_tpo_cliente = models.ForeignKey(TpoCliente, on_delete=models.CASCADE, default=1)
    dni_garante = models.ForeignKey(Garante, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre_cliente

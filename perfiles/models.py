from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, blank=True)
    web = models.URLField(blank=True)
    rut = models.CharField(max_length=20, blank=True, null=True)
    camara_comercio = models.CharField(max_length=20, blank=True, null=True)
    cedula_rl = models.CharField(max_length=20, blank=True, null=True)
    certificado_bancario = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.usuario.username


@receiver(post_save, sender=User)
def crear_usuario_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)


@receiver(post_save, sender=User)
def guardar_usuario_perfil(sender, instance, **kwargs):
    instance.perfil.save()


class Solicitud(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    cantidad = models.IntegerField()
    destino = models.CharField(max_length=255)
    tipo = models.CharField(max_length=50)
    observaciones = models.TextField(blank=True, null=True)
    solicitado = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Orden(models.Model):
    descripcion = models.TextField()
    codigo_cotizacion = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    empresa = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    tiempo_entrega = models.CharField(max_length=255)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.codigo_cotizacion} - {self.descripcion}"


class Anticipo(models.Model):
    nit = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    centro_costo = models.CharField(max_length=50)
    producto_servicio = models.CharField(max_length=100)
    vlr_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    retencion = models.DecimalField(max_digits=10, decimal_places=2)
    total_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Cálculos basados en los valores actuales del formulario
        self.subtotal = self.cantidad * self.vlr_unitario
        self.iva = self.subtotal * self.iva  # Aquí puede haber un problema
        self.retencion = self.subtotal * self.retencion  # Aquí también
        self.total_pagar = self.subtotal + self.iva - self.retencion
        super(Anticipo, self).save(*args, **kwargs)


class AnticipoForm(forms.ModelForm):
    class Meta:
        model = Anticipo
        fields = [
            "nit",
            "nombre",
            "cantidad",
            "centro_costo",
            "producto_servicio",
            "vlr_unitario",
            "subtotal",
            "iva",
            "retencion",
            "total_pagar",
            "observaciones",
        ]

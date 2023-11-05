from django.db import models
from users.models import Client

from .constants.device_constants import DEVICE_CATEGORIES


class DeviceBrand(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre de la marca")
    icon = models.ImageField(
        upload_to="checkit/brands",
        null=True,
        blank=True,
        verbose_name="Icono de la marca",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Marca de dispositivo"
        verbose_name_plural = "Marcas de dispositivos"
        db_table = "device_brand"


class Device(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre del dispositivo")
    serial = models.CharField(
        max_length=50, unique=True, null=True, blank=True, verbose_name="Serial"
    )
    description = models.TextField(null=True, blank=True, verbose_name="Descripción")
    category = models.CharField(
        max_length=200,
        choices=DEVICE_CATEGORIES,
        default=DEVICE_CATEGORIES[0][0],
        verbose_name="Categoría",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    updated_at = models.DateTimeField(
        default=None, null=True, blank=True, verbose_name="Actualizado el"
    )
    owner = models.ForeignKey(
        Client, on_delete=models.CASCADE, blank=False, verbose_name="Dueño"
    )
    brand = models.ForeignKey(
        DeviceBrand, on_delete=models.CASCADE, blank=False, verbose_name="Marca"
    )
    picture = models.ImageField(
        upload_to="checkit/devices",
        null=True,
        blank=True,
        verbose_name="Imagen del dispositivo",
    )
    adquisition_date = models.DateField(
        null=True, blank=True, verbose_name="Fecha de adquisición"
    )
    
    def __str__(self):
        return f"{self.name} - {self.owner}"

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"
        db_table = "device"

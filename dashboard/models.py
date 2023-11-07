from django.db import models
from users.models import Client, Enterprise

from .constants.device_constants import DEVICE_CATEGORIES, MAINTENANCE_STATUS


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
    status = models.BooleanField(
        default=True, verbose_name="¿El dispositivo está activo?"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"
        db_table = "device"


class DeviceMaintenance(models.Model):
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, blank=False, verbose_name="Dispositivo"
    )
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, blank=False, verbose_name="Cliente"
    )
    enterprise = models.ForeignKey(
        Enterprise, on_delete=models.CASCADE, blank=False, verbose_name="Empresa"
    )
    technician_feedback = models.TextField(
        null=True, blank=True, verbose_name="Feedback del técnico"
    )
    reason = models.TextField(
        null=True, blank=True, verbose_name="Motivo de mantenimiento"
    )
    ticket = models.CharField(
        max_length=50, unique=True, null=True, blank=True, verbose_name="Ticket"
    )
    deadline = models.DateField(null=True, blank=True, verbose_name="Fecha límite")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    status = models.CharField(
        max_length=50,
        choices=MAINTENANCE_STATUS,
        default=MAINTENANCE_STATUS[0][0],
        verbose_name="Estado",
    )

    def __str__(self):
        return f"{self.device} - {self.enterprise.enterprise_name} - {self.ticket}"

    class Meta:
        verbose_name = "Mantenimiento de dispositivo"
        verbose_name_plural = "Mantenimientos de dispositivos"
        db_table = "device_maintenance"

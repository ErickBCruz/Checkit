from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_image = models.ImageField(
        upload_to="checkit/profile-pictures",
        blank=True,
        null=True,
        verbose_name="Imagen de perfil",
    )

    class Meta:
        db_table = "user"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class BaseEntity(models.Model):
    address = models.CharField(
        max_length=100,
        verbose_name="Dirección",
    )
    phone = models.CharField(
        max_length=100,
        verbose_name="Numero de Teléfono",
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Latitud",
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Longitud",
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuario",
    )

    class Meta:
        abstract = True


class Enterprise(BaseEntity):
    enterprise_name = models.CharField(
        max_length=100,
        verbose_name="Nombre de la empresa",
        default="Sin registrar",
        unique=True
    )
    nit = models.CharField(
        max_length=100,
        verbose_name="NIT de la entidad",
    )
    slogan = models.CharField(
        max_length=100,
        verbose_name="Slogan",
    )
    foundation_date = models.DateField(
        verbose_name="Fecha de fundación",
    )    
    
    def __str__(self):
        return f"Empresa {self.enterprise_name}"
    class Meta:
        db_table = "enterprise"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"


class Client(BaseEntity):
    document = models.CharField(
        max_length=100,
        verbose_name="Numero de cedula",
    )
    birthday = models.DateField(
        verbose_name="Fecha de nacimiento",
    )
    class Meta:
        db_table = "client"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

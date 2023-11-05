from datetime import date
from django import forms

from users.models import Client

from users.services.client_service import ClientService
from users.services.user_service import UserService


class ClientRegisterForm(forms.ModelForm):
    __client_service = ClientService()
    __user_service = UserService()

    class Meta:
        model = Client
        fields = ["document", "birthday", "address", "phone", "latitude", "longitude"]

    first_name = forms.CharField(
        max_length=100,
        label="Nombres",
        widget=forms.TextInput(
            attrs={"placeholder": "Nombre", "class": "form-control"}
        ),
    )

    last_name = forms.CharField(
        max_length=100,
        label="Apellidos",
        widget=forms.TextInput(
            attrs={"placeholder": "Apellido", "class": "form-control"}
        ),
    )

    document = forms.CharField(
        max_length=100,
        label="Documento",
        widget=forms.TextInput(
            attrs={"placeholder": "Documento", "class": "form-control"}
        ),
    )

    address = forms.CharField(
        max_length=100,
        label="Dirección",
        widget=forms.TextInput(
            attrs={"placeholder": "Dirección", "class": "form-control"}
        ),
    )

    birthday = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )

    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.TextInput(
            attrs={"placeholder": "Correo electrónico", "class": "form-control"}
        ),
    )

    phone = forms.CharField(
        label="Teléfono",
        widget=forms.TextInput(
            attrs={"placeholder": "Teléfono", "class": "form-control"}
        ),
    )

    latitude = forms.DecimalField(
        max_digits=9,
        decimal_places=6,
        label="Latitud",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Latitud",
                "class": "form-control",
                "readonly": True,
                "title": "Es importante que permita el acceso a su ubicación para que el sistema pueda encontra empresas cercanas a usted.",
            }
        ),
    )

    longitude = forms.DecimalField(
        max_digits=9,
        decimal_places=6,
        label="Longitud",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Longitud",
                "class": "form-control",
                "readonly": True,
                "title": "Es importante que permita el acceso a su ubicación para que el sistema pueda encontra empresas cercanas a usted.",
            }
        ),
    )

    profile_image = forms.ImageField(
        label="Imagen de perfil",
        widget=forms.FileInput(attrs={"class": "form-control"}),
        required=False,
    )

    username = forms.CharField(
        max_length=100,
        label="Nombre de usuario",
        widget=forms.TextInput(
            attrs={"placeholder": "Nombre de usuario", "class": "form-control"}
        ),
    )

    password = forms.CharField(
        max_length=100,
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Contraseña", "class": "form-control"}
        ),
    )

    password2 = forms.CharField(
        max_length=100,
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirmar contraseña", "class": "form-control"}
        ),
    )

    widget = {
        "birthday": forms.TextInput(
            attrs={"placeholder": "Fecha de nacimiento", "class": "form-control"}
        ),
    }

    def is_valid(self) -> bool:
        valid = super(ClientRegisterForm, self).is_valid()
        if not valid:
            print(self.errors)
        return valid

    def save(self, commit=True):
        user = self.__user_service.createUser(**self.cleaned_data)
        
        client_data = self.cleaned_data
        client_data["user"] = user
        client = self.__client_service.createClient(**self.cleaned_data)

        if commit:
            user.save()
            client.save()
        else:
            user.delete()
            client.delete()
        return client

    def clean(self):
        cleaned_data = super(ClientRegisterForm, self).clean()

        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

from django import forms
from ...models import Enterprise
from ...services.user_service import UserService

userService = UserService()

class EnterpriseRegisterForm(forms.ModelForm):
    class Meta:
        model = Enterprise
        fields = [
            "enterprise_name",
            "nit",
            "slogan",
            "type",
            "address",
            "phone",
            "latitude",
            "longitude",
        ]

    enterprise_name = forms.CharField(
        max_length=100,
        label="Nombre de la empresa",
        widget=forms.TextInput(
            attrs={"placeholder": "Nombre de la empresa", "class": "form-control"}
        ),
    )

    nit = forms.CharField(
        max_length=100,
        label="NIT",
        widget=forms.TextInput(attrs={"placeholder": "NIT", "class": "form-control"}),
    )

    slogan = forms.CharField(
        max_length=100,
        label="Slogan",
        widget=forms.TextInput(
            attrs={"placeholder": "Slogan", "class": "form-control"}
        ),
    )

    type = forms.CharField(
        max_length=100,
        label="Tipo de empresa",
        widget=forms.TextInput(
            attrs={"placeholder": "Tipo de empresa", "class": "form-control"}
        ),
    )

    address = forms.CharField(
        max_length=100,
        label="Dirección",
        widget=forms.TextInput(
            attrs={"placeholder": "Dirección", "class": "form-control"}
        ),
    )

    phone = forms.CharField(
        max_length=100,
        label="Teléfono",
        widget=forms.TextInput(
            attrs={"placeholder": "Teléfono", "class": "form-control"}
        ),
    )

    first_name = forms.CharField(
        max_length=100,
        label="Nombres del representante legal",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nombres del representante legal",
                "class": "form-control",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=100,
        label="Apellidos del representante legal",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Apellidos del representante legal",
                "class": "form-control",
            }
        ),
    )

    foundation_date = forms.DateField(
        label="Fecha de fundación",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
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

    latitude = forms.DecimalField(
        max_digits=9,
        decimal_places=6,
        label="Latitud",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Latitud",
                "class": "form-control",
                "readonly": True,
                "title": "Es importante que permita el acceso a su ubicación para que el sistema pueda registrar su ubicación actual.",
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
                "title": "Es importante que permita el acceso a su ubicación para que el sistema pueda registrar su ubicación actual.",
            }
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

    widgets = {
        "foundation_date": forms.DateInput(attrs={"type": "date"}),
    }

    def save(self, commit=True):

        user = userService.createUser(
            username=self.cleaned_data["username"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            profile_image=self.cleaned_data["profile_image"],
            password=self.cleaned_data["password"],
        )

        enterprise = Enterprise.objects.create(
            enterprise_name=self.cleaned_data["enterprise_name"],
            nit=self.cleaned_data["nit"],
            slogan=self.cleaned_data["slogan"],
            foundation_date=self.cleaned_data["foundation_date"],
            latitude=self.cleaned_data["latitude"],
            longitude=self.cleaned_data["longitude"],
            type=self.cleaned_data["type"],
            address=self.cleaned_data["address"],
            phone=self.cleaned_data["phone"],
            user=user,
        )

        if commit:
            enterprise.save()
            user.save()
        return enterprise

    def clean(self):
        cleaned_data = super(EnterpriseRegisterForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(EnterpriseRegisterForm, self).__init__(*args, **kwargs)
        self.fields["type"].widget = forms.Select(choices=Enterprise.ENTERPRISE_TYPE)

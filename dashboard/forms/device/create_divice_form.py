from dashboard.models import Device
from django import forms
from dashboard.constants.device_constants import DEVICE_CATEGORIES


class CreateDeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = [
            "name",
            "serial",
            "description",
            "category",
            "brand",
            "picture",
            "adquisition_date",
        ]

    name = forms.CharField(
        label="Nombre del dispositivo",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nombre del dispositivo",
            }
        ),
    )

    serial = forms.CharField(
        label="Serial",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Serial",
            }
        ),
    )

    description = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Descripción", "rows": "2"}
        ),
    )

    category = forms.ChoiceField(
        label="Categoría",
        choices=DEVICE_CATEGORIES,
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    brand = forms.CharField(
        label="Marca",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Marca",
            }
        ),
    )

    picture = forms.ImageField(
        label="Imagen del dispositivo",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "placeholder": "Imagen del dispositivo",
            }
        ),
    )
    adquisition_date = forms.DateField(
        label="Fecha de adquisición",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "Fecha de adquisición",
                "type": "date", 
            }
        ),
    )

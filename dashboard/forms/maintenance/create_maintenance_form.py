from dashboard.models import DeviceMaintenance, Device, Client, Enterprise
from django import forms


from django.forms.widgets import Select
from django.db.models import Q


class DeviceImageWidget(Select):
    def render_option(self, selected_choices, option_value, option_label):
        # Obtén el objeto Device asociado al option_value
        device = Device.objects.get(pk=option_value)
        # Crea un elemento <img> con la URL de la imagen del dispositivo como atributo src
        image_html = (
            f'<img src="{device.image.url}" width="50" height="50" alt="{device.name}">'
        )
        # Devuelve la opción renderizada con la imagen
        return f'<option value="{option_value}"{" selected" if option_value in selected_choices else ""}>{image_html} {option_label}</option>'


class CreateDeviceMaintenance(forms.ModelForm):
    class Meta:
        model = DeviceMaintenance
        fields = [
            "device",
            "client",
            "enterprise",
            "reason",
            "ticket",
        ]

        device = forms.ModelChoiceField(
            queryset=Device.objects.filter(status=True),
            empty_label="Selecciona un dispositivo",
            label="Dispositivo",
            widget=forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "device",
                }
            ),
        )

        client = forms.ModelChoiceField(
            queryset=Client.objects.all(),
            label="Cliente",
            widget=forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "client",
                }
            ),
        )

        reason = forms.CharField(
            label="Motivo de mantenimiento",
            widget=forms.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "reason",
                    "rows": "2",
                }
            ),
            required=True,
        )

        ticket = forms.CharField(
            label="Ticket",
            widget=forms.TextInput(
                attrs={
                    "class": "form-control",
                    "id": "ticket",
                }
            ),
        )

    """_summary_
    Constructor de la clase CreateDeviceMaintenance
    _description_
    Recibe los parámetros:
    - client: Cliente que solicita el mantenimiento
    - enterprise: Empresa a la que se le solicita el mantenimiento
    - ticket: Número de ticket del mantenimiento
    """
    def __init__(self, client, enterprise, ticket, *args, **kwargs):
        super(CreateDeviceMaintenance, self).__init__(*args, **kwargs)
        filtered_devices = Device.objects.filter(
            Q(devicemaintenance__isnull=True)
            | ~Q(devicemaintenance__status__in=["1", "2", "3"]),
            owner=client,
            status=True,
        )  # Filtra los dispositivos que no tienen mantenimiento o que tienen un mantenimiento en estado 1, 2 o 3

        self.fields["device"].queryset = filtered_devices
        self.fields["device"].empty_label = "Selecciona un dispositivo"
        self.fields["device"].label = "Dispositivo"
        self.fields["device"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "device",
            }
        )
        self.fields["client"].queryset = Client.objects.filter(id=client.id)
        self.fields["client"].initial = client
        self.fields["client"].disabled = True
        self.fields["client"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "client",
            }
        )

        self.fields["enterprise"].queryset = Enterprise.objects.filter(id=enterprise.id)
        self.fields["enterprise"].initial = enterprise
        self.fields["enterprise"].disabled = True
        self.fields["enterprise"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "enterprise",
            }
        )

        self.fields["reason"].label = "Motivo de mantenimiento"
        self.fields["reason"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "reason",
                "rows": "2",
            }
        )

        self.fields["ticket"].label = "Ticket"
        self.fields["ticket"].initial = ticket
        self.fields["ticket"].disabled = True
        self.fields["ticket"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "ticket",
            }
        )

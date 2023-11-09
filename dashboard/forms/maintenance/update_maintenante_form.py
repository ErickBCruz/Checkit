from dashboard.models import DeviceMaintenance, Device, Client
from dashboard.constants.device_constants import MAINTENANCE_STATUS
from django import forms


from django.db.models import Q


class UpdateDeviceMaintenanceForm(forms.ModelForm):
    class Meta:
        model = DeviceMaintenance
        fields = [
            "device",
            "client",
            "enterprise",
            "reason",
            "technician_feedback",
            "deadline",
            "status",
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

        status = forms.ChoiceField(
            label="Estado",
            choices=MAINTENANCE_STATUS,
            widget=forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "status",
                }
            ),
        )

        reason = forms.CharField(
            label="Motivo de mantenimiento",
            widget=forms.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "reason",
                    "rows": "5",
                }
            ),
            required=True,
        )

        technician_feedback = forms.CharField(
            label="Tu feedback",
            widget=forms.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "technician_feedback",
                    "rows": "5",
                }
            ),
            required=True,
        )

        deadline = forms.DateField(
            label="Fecha límite",
            widget=forms.DateInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Fecha límite",
                    "type": "date",
                }
            ),
            required=True,
        )

        widgets = {
            "deadline": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "id": "deadline",
                    "type": "date",
                }
            ),
        }

    def __init__(self, maintenance, *args, **kwargs):
        super(UpdateDeviceMaintenanceForm, self).__init__(*args, **kwargs)

        self.fields["device"].initial = maintenance.device
        self.fields["device"].empty_label = "Selecciona un dispositivo"
        self.fields["device"].label = "Dispositivo"
        self.fields["device"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "device",
            }
        )
        self.fields["device"].disabled = True

        self.fields["client"].initial = maintenance.client
        self.fields["client"].disabled = True
        self.fields["client"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "client",
            }
        )

        self.fields["enterprise"].initial = maintenance.enterprise
        self.fields["enterprise"].disabled = True
        self.fields["enterprise"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "enterprise",
            }
        )

        self.fields["reason"].initial = maintenance.reason
        self.fields["reason"].label = "Motivo de mantenimiento"
        self.fields["reason"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "reason",
                "rows": "6",
            }
        )
        self.fields["reason"].disabled = True

        self.fields["deadline"].initial = maintenance.deadline.strftime("%Y-%m-%d")
        self.fields["deadline"].label = "Fecha límite"
        self.fields["deadline"].widget.attrs.update(
            {"class": "form-control", "id": "deadline", "type": "date"}
        )
        self.fields["deadline"].type = "date"
        self.fields["deadline"].disabled = False
        self.fields["deadline"].required = True

        self.fields["status"].choices = [
            (key, value) for key, value in MAINTENANCE_STATUS if key != "1"
        ]
        if maintenance.status not in dict(MAINTENANCE_STATUS).keys():
            maintenance.status = None
        self.fields["status"].initial = maintenance.status
        self.fields["status"].label = "Estado"
        self.fields["status"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "status",
            }
        )

        self.fields["technician_feedback"].initial = maintenance.technician_feedback
        self.fields[
            "technician_feedback"
        ].label = "Retroalimentación técnica del mantenimiento"
        self.fields["technician_feedback"].widget.attrs.update(
            {
                "class": "form-control",
                "id": "technician_feedback",
                "rows": "6",
            }
        )
        self.fields["technician_feedback"].required = True

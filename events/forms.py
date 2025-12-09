# events/forms.py

from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    """
    Formulario para crear / editar eventos.
    """

    class Meta:
        model = Event
        fields = [
            "titulo",
            "descripcion",
            "localidad",
            "fecha_inicio",
            "fecha_termino",
            "hora_inicio",
            "hora_termino",
            "lugar",
            "direccion",
            "imagen",
            "cupos_totales",
            "precio_entrada",   # valor de la entrada
            "solo_mayores_18",  # <<< IMPORTANTE: incluir este campo
        ]

        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "ev-input",
                    "placeholder": "Ej: Taller de reciclaje para vecinos",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "ev-textarea",
                    "rows": 4,
                    "placeholder": "Describe brevemente el evento...",
                }
            ),
            "localidad": forms.TextInput(
                attrs={
                    "class": "ev-input",
                    "placeholder": "Ej: La Florida, Maipú, Puente Alto",
                }
            ),
            "fecha_inicio": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"class": "ev-input", "type": "date"},
            ),
            "fecha_termino": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"class": "ev-input", "type": "date"},
            ),
            "hora_inicio": forms.TimeInput(
                format="%H:%M",
                attrs={"class": "ev-input", "type": "time"},
            ),
            "hora_termino": forms.TimeInput(
                format="%H:%M",
                attrs={"class": "ev-input", "type": "time"},
            ),
            "lugar": forms.TextInput(
                attrs={
                    "class": "ev-input",
                    "placeholder": "Sede vecinal, cancha, plaza, etc.",
                }
            ),
            "direccion": forms.TextInput(
                attrs={
                    "class": "ev-input",
                    "placeholder": "Calle, número y referencias",
                }
            ),
            "imagen": forms.ClearableFileInput(
                attrs={"class": "ev-input-file"}
            ),
            "cupos_totales": forms.NumberInput(
                attrs={"class": "ev-input", "min": 0}
            ),
            "precio_entrada": forms.NumberInput(
                attrs={
                    "class": "ev-input",
                    "min": 0,
                    "step": 1,
                    "placeholder": "0 = gratuito",
                }
            ),
            "solo_mayores_18": forms.CheckboxInput(
                attrs={
                    # si quieres puedes agregar clase CSS
                    # "class": "ev-checkbox-input"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fecha_inicio"].input_formats = ["%Y-%m-%d"]
        self.fields["fecha_termino"].input_formats = ["%Y-%m-%d"]
        self.fields["hora_inicio"].input_formats = ["%H:%M"]
        self.fields["hora_termino"].input_formats = ["%H:%M"]

    def clean(self):
        cleaned = super().clean()
        fecha_inicio = cleaned.get("fecha_inicio")
        fecha_termino = cleaned.get("fecha_termino")

        if fecha_inicio and fecha_termino and fecha_termino < fecha_inicio:
            self.add_error(
                "fecha_termino",
                "La fecha de término no puede ser anterior a la fecha de inicio.",
            )
        return cleaned


class CheckoutForm(forms.Form):
    """
    Formulario de datos del comprador en el checkout.
    (Solo datos de ejemplo, no se hace pago real.)
    """

    nombre = forms.CharField(
        label="Nombre y apellido",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "ev-input", "placeholder": "Nombre y apellido"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "ev-input", "placeholder": "Ingresa tu correo electrónico"}
        ),
    )
    email_confirmacion = forms.EmailField(
        label="Repetir email",
        widget=forms.EmailInput(
            attrs={"class": "ev-input", "placeholder": "Repite tu correo electrónico"}
        ),
    )
    telefono = forms.CharField(
        label="Celular",
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "ev-input", "placeholder": "Tu celular, ejemplo: 999999999"}
        ),
    )

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        email_confirmacion = cleaned.get("email_confirmacion")

        if email and email_confirmacion and email != email_confirmacion:
            self.add_error(
                "email_confirmacion",
                "Los correos electrónicos no coinciden.",
            )

        return cleaned

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil
from .models import Solicitud
from .models import Orden
from .models import Anticipo


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=140,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        max_length=140,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    rut = forms.FileField(
        required=True, widget=forms.FileInput(attrs={"class": "form-control"})
    )
    camara_comercio = forms.FileField(
        required=True, widget=forms.FileInput(attrs={"class": "form-control"})
    )
    cedula_rl = forms.FileField(
        required=True, widget=forms.FileInput(attrs={"class": "form-control"})
    )
    certificado_bancario = forms.FileField(
        required=True, widget=forms.FileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "rut",
            "camara_comercio",
            "cedula_rl",
            "certificado_bancario",
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            # Guardar el perfil asociado con los archivos subidos
            Perfil.objects.create(
                usuario=user,
                rut=self.cleaned_data["rut"],
                camara_comercio=self.cleaned_data["camara_comercio"],
                cedula_rl=self.cleaned_data["cedula_rl"],
                certificado_bancario=self.cleaned_data["certificado_bancario"],
            )
        return user


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            "nombre",
            "descripcion",
            "cantidad",
            "destino",
            "tipo",
            "observaciones",
            "solicitado",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "required": True}
            ),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "required": True}
            ),
            "cantidad": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "required": True}
            ),
            "destino": forms.Select(attrs={"class": "form-control", "required": True}),
            "tipo": forms.Select(attrs={"class": "form-control", "required": True}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "solicitado": forms.TextInput(
                attrs={"class": "form-control", "required": True}
            ),
        }


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = [
            "descripcion",
            "codigo_cotizacion",
            "precio",
            "cantidad",
            "empresa",
            "destino",
            "tiempo_entrega",
            "observaciones",
        ]
        labels = {
            "descripcion": "Descripción del Producto o Servicio",
            "codigo_cotizacion": "# de Código o # de Cotización",
            "precio": "Precio",
            "cantidad": "Cantidad",
            "empresa": "Empresa",
            "destino": "Destino de Producto o Servicio",
            "tiempo_entrega": "Tiempo de Entrega",
            "observaciones": "Observaciones",
        }
        help_texts = {
            "codigo_cotizacion": "Ingrese el número de código o cotización.",
        }
        widgets = {
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "required": True}
            ),
            "codigo_cotizacion": forms.TextInput(attrs={"class": "form-control"}),
            "precio": forms.NumberInput(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "required": True}
            ),
            "empresa": forms.TextInput(attrs={"class": "form-control"}),
            "destino": forms.Select(attrs={"class": "form-control", "required": True}),
            "tiempo_entrega": forms.TextInput(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


def clean_precio(self):
    precio = self.cleaned_data.get("precio")
    if precio <= 0:
        raise forms.ValidationError("El precio debe ser mayor que cero.")
    return precio


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
        widgets = {
            "nit": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "required": True}
            ),
            "cantidad": forms.NumberInput(
                attrs={"class": "form-control", "min": "1", "required": True}
            ),
            "centro_costo": forms.Select(
                attrs={"class": "form-control", "required": True}
            ),
            "producto_servicio": forms.TextInput(
                attrs={"class": "form-control", "required": True}
            ),
            "vlr_unitario": forms.NumberInput(
                attrs={"class": "form-control", "required": True}
            ),
            "subtotal": forms.NumberInput(
                attrs={"class": "form-control", "readonly": True}
            ),
            "iva": forms.NumberInput(attrs={"class": "form-control", "required": True}),
            "retencion": forms.NumberInput(
                attrs={"class": "form-control", "required": True}
            ),
            "total_pagar": forms.NumberInput(
                attrs={"class": "form-control", "readonly": True}
            ),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

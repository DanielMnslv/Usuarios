from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil


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
            perfil = Perfil.objects.create(
                usuario=user,
                rut=self.cleaned_data["rut"],
                camara_comercio=self.cleaned_data["camara_comercio"],
                cedula_rl=self.cleaned_data["cedula_rl"],
                certificado_bancario=self.cleaned_data["certificado_bancario"],
            )
        return user

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.views.generic import CreateView, TemplateView

from .models import Perfil

from .forms import SignUpForm
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.db import transaction
from django.urls import reverse_lazy
from django.urls import reverse
from .models import Solicitud
from .forms import SolicitudForm
from .forms import OrdenForm
from django.views import View
from .forms import AnticipoForm
from .models import Anticipo


class SignUpView(CreateView):
    model = Perfil
    form_class = SignUpForm
    template_name = "registration/register.html"

    def form_valid(self, form):
        try:
            # Save the user first
            user = form.save()

            # Check if the profile already exists
            if not Perfil.objects.filter(usuario=user).exists():
                # Create the profile for the user
                Perfil.objects.create(
                    usuario=user,
                    rut=form.cleaned_data.get("rut"),
                    camara_comercio=form.cleaned_data.get("camara_comercio"),
                    cedula_rl=form.cleaned_data.get("cedula_rl"),
                    certificado_bancario=form.cleaned_data.get("certificado_bancario"),
                )

            # Authenticate the user
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(self.request, user)
                return redirect("/")

        except IntegrityError:
            # Handle or log the exception
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("login")


class BienvenidaView(TemplateView):
    template_name = "perfiles/bienvenida.html"


class SignInView(LoginView):
    template_name = "perfiles/iniciar_sesion.html"

    def get_success_url(self):
        return reverse_lazy("bienvenida")


class SolicitudView(TemplateView):
    template_name = "perfiles/solicitud.html"


class OrdenView(TemplateView):
    template_name = "perfiles/orden.html"


class AnticipoView(TemplateView):
    template_name = "perfiles/anticipo.html"


class DiarioView(TemplateView):
    template_name = "perfiles/diario.html"


class SolicitudView(View):
    def get(self, request):
        form = SolicitudForm()
        return render(request, "perfiles/solicitud.html", {"form": form})

    def post(self, request):
        form = SolicitudForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("bienvenida")
        return render(request, "perfiles/solicitud.html", {"form": form})


class OrdenView(View):
    def get(self, request):
        form = OrdenForm()
        return render(request, "perfiles/orden.html", {"form": form})

    def post(self, request):
        form = OrdenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("bienvenida")
        return render(request, "perfiles/orden.html", {"form": form})


def anticipo_view(request):
    if request.method == "POST":
        form = AnticipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("bienvenida")
        else:
            print(form.errors)  # Esto te ayudará a ver cualquier error en la consola
    else:
        form = AnticipoForm()

    return render(request, "perfiles/anticipo.html", {"form": form})

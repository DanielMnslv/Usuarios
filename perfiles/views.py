from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from django.views.generic import CreateView, TemplateView

from .models import Perfil

from .forms import SignUpForm
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.db import transaction
from django.urls import reverse_lazy
from django.urls import reverse
from .models import Solicitud
from .models import Orden
from .forms import SolicitudForm
from .forms import OrdenForm
from django.views import View
from .forms import AnticipoForm
from .forms import DiarioForm
from .models import Anticipo
from .forms import DiarioForm
from .models import Diario
from django.core.paginator import Paginator


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
            return redirect("bienvenida")  # Ensure this URL exists in your project
        else:
            print(form.errors)  # Debug any form errors
    else:
        form = AnticipoForm()

    return render(request, "perfiles/anticipo.html", {"form": form})


def diario_view(request):
    if request.method == "POST":
        form = DiarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(
                "bienvenida"
            )  # Redirige a una página de éxito o lista de órdenes
    else:
        form = DiarioForm()

    return render(request, "perfiles/diario.html", {"form": form})


def ver_solicitudes(request):
    solicitudes = Solicitud.objects.all()

    # Filtrar por los campos
    id_filtro = request.GET.get("id")
    nombre_filtro = request.GET.get("nombre")
    descripcion_filtro = request.GET.get("descripcion")
    cantidad_filtro = request.GET.get("cantidad")
    destino_filtro = request.GET.get("destino")
    tipo_filtro = request.GET.get("tipo")
    solicitado_filtro = request.GET.get("solicitado")

    if id_filtro:
        solicitudes = solicitudes.filter(id=id_filtro)
    if nombre_filtro:
        solicitudes = solicitudes.filter(nombre__icontains=nombre_filtro)
    if descripcion_filtro:
        solicitudes = solicitudes.filter(descripcion__icontains=descripcion_filtro)
    if cantidad_filtro:
        solicitudes = solicitudes.filter(cantidad=cantidad_filtro)
    if destino_filtro:
        solicitudes = solicitudes.filter(destino__icontains=destino_filtro)
    if tipo_filtro:
        solicitudes = solicitudes.filter(tipo__icontains=tipo_filtro)
    if solicitado_filtro:
        solicitudes = solicitudes.filter(solicitado__icontains=solicitado_filtro)

    # Paginación
    paginator = Paginator(solicitudes, 10)  # Muestra 10 solicitudes por página
    page_number = request.GET.get("page")
    solicitudes_page = paginator.get_page(page_number)

    return render(request, "ver_solicitudes.html", {"solicitudes": solicitudes_page})


def ver_ordenes(request):
    ordenes = Orden.objects.all()

    # Filtrar por los campos
    id_filtro = request.GET.get("id")
    descripcion_filtro = request.GET.get("descripcion")
    codigo_cotizacion_filtro = request.GET.get("codigo_cotizacion")
    precio_filtro = request.GET.get("precio")
    cantidad_filtro = request.GET.get("cantidad")
    empresa_filtro = request.GET.get("empresa")
    destino_filtro = request.GET.get("destino")
    tiempo_entrega_filtro = request.GET.get("tiempo_entrega")
    observaciones_filtro = request.GET.get("observaciones")

    if id_filtro:
        ordenes = ordenes.filter(id=id_filtro)
    if descripcion_filtro:
        ordenes = ordenes.filter(descripcion__icontains=descripcion_filtro)
    if codigo_cotizacion_filtro:
        ordenes = ordenes.filter(codigo_cotizacion__icontains=codigo_cotizacion_filtro)
    if precio_filtro:
        ordenes = ordenes.filter(precio=precio_filtro)
    if cantidad_filtro:
        ordenes = ordenes.filter(cantidad=cantidad_filtro)
    if empresa_filtro:
        ordenes = ordenes.filter(empresa__icontains=empresa_filtro)
    if destino_filtro:
        ordenes = ordenes.filter(destino__icontains=destino_filtro)
    if tiempo_entrega_filtro:
        ordenes = ordenes.filter(tiempo_entrega__icontains=tiempo_entrega_filtro)
    if observaciones_filtro:
        ordenes = ordenes.filter(observaciones__icontains=observaciones_filtro)

    # Paginación
    paginator = Paginator(ordenes, 10)  # Muestra 10 órdenes por página
    page_number = request.GET.get("page")
    ordenes_page = paginator.get_page(page_number)

    return render(request, "ver_ordenes.html", {"ordenes": ordenes_page})


def ver_diario(request):
    diario = Diario.objects.all()

    # Filtrar por los campos
    id_filtro = request.GET.get("id")
    tiempo_entrega_filtro = request.GET.get("tiempo_entrega")
    nombre_filtro = request.GET.get("nombre")
    empresa_filtro = request.GET.get("empresa")
    centro_costo_filtro = request.GET.get("centro_costo")
    destino_filtro = request.GET.get("destino")
    medio_pago_filtro = request.GET.get("medio_pago")
    documento_pdf_filtro = request.GET.get("documento_pdf")

    if id_filtro:
        diario = diario.filter(id=id_filtro)
    if tiempo_entrega_filtro:
        diario = diario.filter(tiempo_entrega__icontains=tiempo_entrega_filtro)
    if nombre_filtro:
        diario = diario.filter(nombre__icontains=nombre_filtro)
    if empresa_filtro:
        diario = diario.filter(empresa=empresa_filtro)
    if centro_costo_filtro:
        diario = diario.filter(centro_costo=centro_costo_filtro)
    if destino_filtro:
        diario = diario.filter(destino__icontains=destino_filtro)
    if medio_pago_filtro:
        diario = diario.filter(medio_pago__icontains=medio_pago_filtro)
    if tiempo_entrega_filtro:
        diario = diario.filter(tiempo_entrega__icontains=tiempo_entrega_filtro)
    if documento_pdf_filtro:
        diario = diario.filter(documento_pdf__icontains=documento_pdf_filtro)

    # Paginación
    paginator = Paginator(diario, 10)  # Muestra 10 órdenes por página
    page_number = request.GET.get("page")
    diario_page = paginator.get_page(page_number)

    return render(request, "ver_diario.html", {"diario": diario_page})


def custom_logout(request):
    logout(request)
    return redirect("login")

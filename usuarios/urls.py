from django.contrib import admin
from django.urls import path
from perfiles.views import (
    SignUpView,
    BienvenidaView,
    SignInView,
    SolicitudView,
    OrdenView,
    AnticipoView,
    DiarioView,
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", BienvenidaView.as_view(), name="bienvenida"),
    path("registrate/", SignUpView.as_view(), name="sign_up"),
    path("login/", SignInView.as_view(), name="login"),
    path("solicitud/", SolicitudView.as_view(), name="solicitud"),
    path("orden/", OrdenView.as_view(), name="orden"),
    path("anticipo/", AnticipoView.as_view(), name="anticipo"),
    path("diario/", DiarioView.as_view(), name="diario"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

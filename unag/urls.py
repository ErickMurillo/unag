"""unag URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from productores.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^login/$', auth_views.login, {'template_name': 'frontend/login.html'}),
    url(r'^logout/$', auth_views.logout,{'next_page': '/'}),
    url(r'^$', index, name='index'),
    url(r'^mapa-index/$', obtener_lista, name='obtener-lista'),
    url(r'^afiliados/$', afiliados, name='afiliados'),
    url(r'^consulta/$', consulta, name='consulta'),
    url(r'^ajax/comunidades/$', get_comunies, name='get-comunies'),
    url(r'^datos-generales/$', datos_generales, name='datos-generales'),
    url(r'^datos-familiares/$', datos_familiares, name='datos-familiares'),
    url(r'^datos-propiedad/$', datos_propiedad, name='datos-propiedad'),
    url(r'^datos-produccion/$', datos_produccion, name='datos-produccion'),
    url(r'^organizacion/$', organizacion, name='organizacion'),
    url(r'^select2/', include('django_select2.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

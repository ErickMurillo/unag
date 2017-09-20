# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from .forms import * 

# Register your models here.
class AfiliadoAdmin(admin.ModelAdmin):
    search_fields = ['nombre','municipio','comunidad']
    list_filter = ['sexo',]
    list_display = ['nombre','cedula','municipio','comunidad']

admin.site.register(Afiliado,AfiliadoAdmin)

class DatosGeneralesInline(admin.TabularInline):
    model = DatosGenerales
    max_num = 1
    can_delete = False

class EscolaridadInline(admin.TabularInline):
    model = Escolaridad
    can_delete = False
    max_num = 1

class ProfesionInline(admin.TabularInline):
    model = Profesion
    max_num = 1
    can_delete = False

class PersonasDependenInline(admin.TabularInline):
    model = PersonasDependen
    max_num = 5
    extra = 1

class DatosFamiliaresInline(admin.TabularInline):
    model = DatosFamiliares
    extra = 1
    form = DatosFamiliaresForm

class FamiliaEmigraInline(admin.TabularInline):
    model = FamiliaEmigra
    max_num = 1
    can_delete = False

class AreasFincaInline(admin.TabularInline):
    model = AreasFinca
    extra = 1

class TierrasAlquiladasInline(admin.TabularInline):
    model = TierrasAlquiladas
    max_num = 1
    can_delete = False

class OtrasTierrasInline(admin.TabularInline):
    model = OtrasTierras
    extra = 1

class OrigenPropiedadInline(admin.TabularInline):
    model = OrigenPropiedad
    max_num = 1
    can_delete = False

class FormaTenenciaInline(admin.TabularInline):
    model = FormaTenencia
    max_num = 1
    can_delete = False

class DocumentoPropiedadInline(admin.TabularInline):
    model = DocumentoPropiedad
    max_num = 1
    can_delete = False

class SistemaAguaInline(admin.TabularInline):
    model = SistemaAgua
    max_num = 1
    can_delete = False

class EnergiaElectricaInline(admin.TabularInline):
    model = EnergiaElectrica
    max_num = 1
    can_delete = False

class InventarioAnimalesInline(admin.TabularInline):
    model = InventarioAnimales
    extra = 1

class ProduccionHuevosLecheInline(admin.TabularInline):
    model = ProduccionHuevosLeche
    extra = 1
    max_num = 8

class AgriculturaInline(admin.TabularInline):
    model = Agricultura
    extra = 1

class ManoObraInline(admin.TabularInline):
    model = ManoObra
    max_num = 1
    can_delete = False

class TablaEmpleoInline(admin.TabularInline):
    model = TablaEmpleo
    extra = 1

class InfraestructuraInline(admin.TabularInline):
    model = Infraestructura
    extra = 1

class CotizacionInline(admin.TabularInline):
    model = Cotizacion
    max_num = 1
    can_delete = False

class RespuestaSiCotizaInline(admin.TabularInline):
    model = RespuestaSiCotiza
    max_num = 1
    can_delete = False

class RespuestaSiCotizaInline(admin.TabularInline):
    model = RespuestaSiCotiza
    max_num = 1
    can_delete = False

class MiembroCooperativaInline(admin.TabularInline):
    model = MiembroCooperativa
    max_num = 1
    can_delete = False

class BeneficiadoProyectoInline(admin.TabularInline):
    model = BeneficiadoProyecto
    max_num = 1
    can_delete = False

class CreditoInline(admin.TabularInline):
    model = Credito
    max_num = 1
    can_delete = False

class CotizacionOrganizacionInline(admin.TabularInline):
    model = CotizacionOrganizacion
    max_num = 1
    can_delete = False

class EncuestaAdmin(admin.ModelAdmin):
    list_display = ['afiliado','fecha_encuesta']
    date_hierarchy = 'fecha_encuesta'
    search_fields = ['afiliado__nombre']
    form = EncuestaAfiliadoForm

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Encuesta.objects.all()
        return Encuesta.objects.filter(usuario=request.user)

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            obj.save()
        else:
            obj.usuario = request.user
            obj.save()

    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            self.exclude = ('usuario',)

        return super(EncuestaAdmin, self).get_form(request, obj=None, **kwargs)

    inlines = [DatosGeneralesInline,EscolaridadInline,ProfesionInline,PersonasDependenInline,
                DatosFamiliaresInline,AreasFincaInline,FormaTenenciaInline,DocumentoPropiedadInline,
                TierrasAlquiladasInline,OtrasTierrasInline,SistemaAguaInline,EnergiaElectricaInline,InventarioAnimalesInline,
                ProduccionHuevosLecheInline,AgriculturaInline,ManoObraInline,
                TablaEmpleoInline,InfraestructuraInline,CotizacionInline,RespuestaSiCotizaInline,
                MiembroCooperativaInline,BeneficiadoProyectoInline,CreditoInline,CotizacionOrganizacionInline]

    class Media:
        css = {
            'all': ('css/admin.css',)
        }
        js = ('plugins/jquery.min.js','js/admin.js',)

admin.site.register(Encuesta,EncuestaAdmin)

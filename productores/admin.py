# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from .forms import * 

# Register your models here.
class AfiliadoAdmin(admin.ModelAdmin):
    search_fields = ['nombre','municipio__nombre','comunidad__nombre']
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

class AcuicolaInline(admin.TabularInline):
    model = Acuicola
    max_num = 1
    can_delete = False

class ApicolaInline(admin.TabularInline):
    model = Apicola
    max_num = 1
    can_delete = False

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

class AgriculturaInline(admin.TabularInline):
    model = Agricultura
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('rubro', 'tipo', 'area_sembrada', 'produccion_total','semillas','consumo_humano','consumo_animal','venta','quien_vende')
        }),
    )

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

class MiembroBancoSemillaInline(admin.TabularInline):
    model = MiembroBancoSemilla
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

from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

class EncuestaAdmin(admin.ModelAdmin):
    list_display = ['afiliado','fecha_encuesta']
    date_hierarchy = 'fecha_encuesta'
    search_fields = ['afiliado__nombre',
                    'sistemaagua__sistema__nombre','tablaempleo__rubro__nombre',
                    'infraestructura__tipo__nombre','respuestasicotiza__donde_cotiza__nombre',
                    'miembrocooperativa__cooperativa__nombre','beneficiadoproyecto__proyectos__nombre',
                    'credito__proyectos__nombre','credito__formas_recibe_credito__nombre',
                    'cotizacionorganizacion__problemas_productor__nombre','cotizacionorganizacion__acciones_cambio_climatico__nombre',
                    'cotizacionorganizacion__afiliacion_unag__nombre']
    list_filter = ('ronda',
    				('areasfinca__areas', RelatedDropdownFilter),
    				('agricultura__rubro',RelatedDropdownFilter),
    				('documentopropiedad__documento',RelatedDropdownFilter),
                    ('areasfinca__origen',RelatedDropdownFilter),
                    ('sistemaagua__sistema',RelatedDropdownFilter),
    				('inventarioanimales__animal',RelatedDropdownFilter),
                    ('infraestructura__tipo',RelatedDropdownFilter),
                    ('respuestasicotiza__donde_cotiza',RelatedDropdownFilter),
                    ('miembrocooperativa__cooperativa',RelatedDropdownFilter),
                    ('beneficiadoproyecto__proyectos',RelatedDropdownFilter),
                    ('credito__proyectos',RelatedDropdownFilter),
                    ('credito__formas_recibe_credito',RelatedDropdownFilter),
                    ('cotizacionorganizacion__acciones_cambio_climatico',RelatedDropdownFilter),
                    ('cotizacionorganizacion__problemas_productor',RelatedDropdownFilter),
                    ('cotizacionorganizacion__afiliacion_unag',RelatedDropdownFilter))
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

    # def get_form(self, request, obj=None, **kwargs):
    #     if not request.user.is_superuser:
    #         self.exclude = ('usuario',)

    #     return super(EncuestaAdmin, self).get_form(request, obj=None, **kwargs)

    inlines = [DatosGeneralesInline,EscolaridadInline,ProfesionInline,
                PersonasDependenInline,FamiliaEmigraInline,
                DatosFamiliaresInline,AreasFincaInline,AcuicolaInline,ApicolaInline,FormaTenenciaInline,DocumentoPropiedadInline,
                TierrasAlquiladasInline,OtrasTierrasInline,SistemaAguaInline,EnergiaElectricaInline,InventarioAnimalesInline,
                ProduccionHuevosLecheInline,AgriculturaInline,ManoObraInline,
                TablaEmpleoInline,InfraestructuraInline,CotizacionInline,RespuestaSiCotizaInline,
                MiembroCooperativaInline,MiembroBancoSemillaInline,BeneficiadoProyectoInline,CreditoInline,CotizacionOrganizacionInline]

    class Media:
        css = {
            'all': ('css/admin.css',)
        }
        js = ('plugins/jquery.min.js','js/admin.js',)

admin.site.register(Encuesta,EncuestaAdmin)

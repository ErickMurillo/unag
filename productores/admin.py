# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
class EscolaridadInline(admin.TabularInline):
    model = Escolaridad
    extra = 1
    max_num = 5

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

class FamiliaEmigraInline(admin.TabularInline):
    model = FamiliaEmigra
    max_num = 1
    can_delete = False

class AfiliadoAdmin(admin.ModelAdmin):
    inlines = [EscolaridadInline,ProfesionInline,PersonasDependenInline,
                DatosFamiliaresInline,FamiliaEmigraInline]
    search_fields = ['nombre',]
    list_filter = ['municipio','comunidad','sexo']
    list_display = ['nombre','cedula','municipio','comunidad']

admin.site.register(Afiliado,AfiliadoAdmin)

class AreasFincaInline(admin.TabularInline):
    model = AreasFinca
    extra = 1

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
    max_num = 2

class AgriculturaInline(admin.TabularInline):
    model = Agricultura
    extra = 1

class VendeProduccionInline(admin.TabularInline):
    model = VendeProduccion
    max_num = 1
    can_delete = False

class EncuestaAdmin(admin.ModelAdmin):
    inlines = [AreasFincaInline,OtrasTierrasInline,OrigenPropiedadInline,FormaTenenciaInline,
                DocumentoPropiedadInline,SistemaAguaInline,InventarioAnimalesInline,ProduccionHuevosLecheInline,
                AgriculturaInline,VendeProduccionInline]

admin.site.register(Encuesta,EncuestaAdmin)
admin.site.register(Areas)
admin.site.register(Origen)
admin.site.register(Documento)
admin.site.register(Sistema)
admin.site.register(Animales)
admin.site.register(Cultivo)
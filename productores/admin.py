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

class AfiliadoAdmin(admin.ModelAdmin):
    inlines = [EscolaridadInline,ProfesionInline,PersonasDependenInline]

admin.site.register(Afiliado,AfiliadoAdmin)

from django.contrib import admin
from models import *
from import_export.admin import ImportExportModelAdmin

class DepartamentoAdmin(ImportExportModelAdmin):
    list_display = ['nombre']
    list_filter = ['nombre']
    # prepopulated_fields = {"slug": ("nombre", )}
    search_fields = ['nombre']

class MunicipioAdmin(ImportExportModelAdmin):
    list_display = ['nombre', 'departamento']
    list_filter = ['departamento']
    search_fields = ['nombre']
    # prepopulated_fields = {"slug": ("nombre", )}

class ComunidadAdmin(ImportExportModelAdmin):
    list_display = ['nombre', 'municipio']
    list_filter = ['municipio']
    search_fields = ['nombre']

#class MicrocuencaAdmin(admin.ModelAdmin):
#    list_display = ['nombre']
#    search_fields = ['nombre']

admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Comunidad, ComunidadAdmin)
#admin.site.register(Microcuenca, MicrocuencaAdmin)
# admin.site.register(Pais)

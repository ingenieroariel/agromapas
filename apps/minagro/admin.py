from django.contrib import admin
from django.contrib import databrowse
from minagro.models import *

class ViviendaAdmin(admin.ModelAdmin):
    list_display = ('radicacion', 'vigencia', 'acta',  'departamento',
            'municipio', 'localidad', 'recursos', 'tipo_solucion', 'hogares', 'avance', 'estado', 'valor_total', 'subsidio', )
    ordering = ('radicacion',)
    list_filter    = ('vigencia', 'departamento', 'tipo_solucion', 'estado')
    search_fields  = ('vigencia','acta', 'radicacion', 'departamento',
            'municipio', 'localidad','causal_demora', 'tipo_solucion',)


class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nombre', )
    search_fields = ('id', 'nombre',)

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ( 'nombre', 'count', 'sum_valor', 'sum_hogares', 
            'avg_avance')
    search_fields = ('nombre',)

#admin.site.register(Municipio, MunicipioAdmin)
admin.site.register(Vivienda, ViviendaAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register([Poblacion, Localidad, ViviendaCode])

databrowse.site.register(Vivienda)


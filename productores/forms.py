# -*- coding: UTF-8 -*-
from django.db import models
from .models import *
from django import forms
from django_select2.forms import *

# def fecha_choice():
#     years = []
#     for en in Encuesta.objects.order_by('anio').values_list('anio', flat=True):
#         years.append((en,en))
#     return list(sorted(set(years)))

RONDA_CHOICES = ((1,'I'),(2,'II'), (3,'III'), 
                    (4,'IV'),(5,'V')
                )
def ronda():
    ronda = []
    for en in Encuesta.objects.order_by('ronda').values_list('ronda', flat=True):
        ronda.append(en)
    #-------

    x = list(sorted(set(ronda)))

    lista_ronda = []
    for r in RONDA_CHOICES:
        if r[0] in x:
            list_anios = []
            for anios in Encuesta.objects.filter(ronda = r[0]).values_list('anio', flat=True):
                list_anios.append(anios)

            lista = list(sorted(set(list_anios)))
            lista_ronda.append((r[0],r[1] + ' ('+str(lista[0])+'-'+str(lista[-1])+')'))
     
    return lista_ronda

def municipios():
    foo = Encuesta.objects.order_by('afiliado__municipio').distinct().values_list('afiliado__municipio__id', flat=True)
    return Municipio.objects.filter(id__in=foo)

SEXO_CHOICES = (('','Ambos'),('Femenino','Femenino'), ('Masculino','Masculino'))

class EncuestaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EncuestaForm, self).__init__(*args, **kwargs)
        self.fields['anio'] = forms.ChoiceField(choices=ronda(),required=True,label='Ronda')
        # self.fields['departamento'] = forms.ModelMultipleChoiceField(queryset=Departamento.objects.all(),required=False,label='Departamentos')
        self.fields['municipio'] = forms.ModelMultipleChoiceField(queryset=municipios(),required=False,label='Municipios')
        self.fields['comunidad'] = forms.ModelMultipleChoiceField(queryset=Comunidad.objects.all(),required=False,label='Comunidades')
        self.fields['sexo'] = forms.ChoiceField(choices=SEXO_CHOICES,required=False,label='Sexo',widget=forms.RadioSelect)
        self.fields['edad_inicio'] = forms.IntegerField(required=False,label='Edad inicio')
        self.fields['edad_fin'] = forms.IntegerField(required=False,label='Edad fin')

class AfiliadoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AfiliadoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'] = forms.ModelChoiceField(queryset=Afiliado.objects.all().order_by('nombre'),required=True,label='Afiliados')

class EncuestaAfiliadoForm(forms.ModelForm):
    class Meta:
        model = Afiliado
        fields = '__all__'
        widgets = {
            'afiliado': Select2Widget
        }

class DatosFamiliaresForm(forms.ModelForm):
    class Meta:
        model = DatosFamiliares
        fields = '__all__'
        widgets = {
            'meses': forms.SelectMultiple()
            }
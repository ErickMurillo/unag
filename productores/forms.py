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

def departamentos():
    foo = Encuesta.objects.order_by('afiliado__municipio__departamento').distinct().values_list('afiliado__municipio__departamento__id', flat=True)
    return Departamento.objects.filter(id__in=foo)

class EncuestaForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EncuestaForm, self).__init__(*args, **kwargs)
        self.fields['anio'] = forms.ChoiceField(choices=ronda(),required=True,label='Ronda')
        self.fields['departamento'] = forms.ModelMultipleChoiceField(queryset=departamentos(),required=False,label='Departamentos')
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

SI_NO_CHOICES = (('','------'),('Si','Si'), ('No','No'))
ESTADO_CIVIL_CHOICES = (('','------'),('Soltero(a)','Soltero(a)'), ('Casado(a)','Casado(a)'), ('Acompañado(a)','Acompañado(a)'),
                        ('Viudo(a)','Viudo(a)'), ('Divorciado(a)','Divorciado(a)'))
ESCOLARIDAD_CHOICES = (('','------'),('Preescolar','Preescolar'),('Primaria','Primaria'),
                        ('Secundaria','Secundaria'), ('Universitario','Universitario'))

class AfiliadoForm2(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AfiliadoForm2, self).__init__(*args, **kwargs)
        self.fields['departamento'] = forms.ModelMultipleChoiceField(queryset=departamentos(),required=False,label='Departamentos')
        self.fields['municipio'] = forms.ModelMultipleChoiceField(queryset=Municipio.objects.all(),required=False,label='Municipios')
        self.fields['comunidad'] = forms.ModelMultipleChoiceField(queryset=Comunidad.objects.all(),required=False,label='Comunidades')
        self.fields['sexo'] = forms.ChoiceField(choices=SEXO_CHOICES,required=False,label='Sexo',widget=forms.RadioSelect)
        self.fields['estado_civil'] = forms.ChoiceField(choices=ESTADO_CIVIL_CHOICES,label='Estado civil',required=False)
        self.fields['escolaridad'] = forms.ChoiceField(choices=SI_NO_CHOICES,label='Escolaridad',required=False)
        self.fields['nivel_escolaridad'] = forms.ChoiceField(choices=ESCOLARIDAD_CHOICES,label='Nivel de Escolaridad',required=False)
        self.fields['internet'] = forms.ChoiceField(choices=SI_NO_CHOICES,label='Acceso a internet',required=False)
        self.fields['cotiza'] = forms.ChoiceField(choices=SI_NO_CHOICES,label='Cotiza',required=False)
        self.fields['cooperativa'] = forms.ChoiceField(choices=SI_NO_CHOICES,label='Miembro cooperativa',required=False)
        self.fields['cooperativas'] = forms.ModelMultipleChoiceField(queryset=Cooperativa.objects.all(),required=False,label='Cooperativas')
        self.fields['proyecto'] = forms.ChoiceField(choices=SI_NO_CHOICES,label='Beneficiado por otros proyectos',required=False)
        self.fields['credito'] = forms.ChoiceField(choices=SI_NO_CHOICES,label='Crédito',required=False)
        self.fields['problemas_productor'] = forms.ModelMultipleChoiceField(queryset=ProblemasProductor.objects.all(),label='Problemas más sentidos',required=False)
        self.fields['cambio_climatico'] = forms.ModelMultipleChoiceField(queryset=CambioClimatico.objects.all(),label='Cambio climático',required=False)
        self.fields['motivos'] = forms.ModelMultipleChoiceField(queryset=AfiliacionUnag.objects.all(),label='Motivos de Afiliación a la UNAG',required=False)
        self.fields['edad_inicio'] = forms.IntegerField(required=False,label='Edad inicio')
        self.fields['edad_fin'] = forms.IntegerField(required=False,label='Edad fin')

FAMILIA_CHOICES = (
    ('Abuela','Abuela'),('Abuelo','Abuelo'),
    ('Bisabuela','Bisabuela'),('Bisabuelo','Bisabuelo'),
    ('Cuniada','Cuñada'),('Cuniado','Cuñado'),
    ('Esposa','Esposa'),('Esposo','Esposo'),
    ('Hermana','Hermana'),('Hermano','Hermano'),
    ('Hija','Hija'),('Hijo','Hijo'),
    ('Madre','Madre'),('Nuera','Nuera'),
    ('Padre','Padre'),('Pareja','Pareja'),
    ('Prima','Prima'),('Primo','Primo'),
    ('Sobrina','Sobrina'),('Sobrino','Sobrino'),
    ('Suegra','Suegra'),('Suegro','Suegro'),
    ('Tia','Tía'),('Tio','Tío'),
    ('Yerno','Yerno'),
    ('Nieto','Nieto'),('Nieta','Nieta'),
    ('Otro','Otro'),
)

class AfiliadoFamiliaresForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AfiliadoFamiliaresForm, self).__init__(*args, **kwargs)
        self.fields['departamento'] = forms.ModelMultipleChoiceField(queryset=departamentos(),required=False,label='Departamentos')
        self.fields['municipio'] = forms.ModelMultipleChoiceField(queryset=Municipio.objects.all(),required=False,label='Municipios')
        self.fields['comunidad'] = forms.ModelMultipleChoiceField(queryset=Comunidad.objects.all(),required=False,label='Comunidades')
        self.fields['sexo'] = forms.ChoiceField(choices=SEXO_CHOICES,required=False,label='Sexo',widget=forms.RadioSelect)
        self.fields['escolaridad'] = forms.ChoiceField(choices=ESCOLARIDAD_CHOICES,label='Escolaridad',required=False)
        self.fields['parentesco'] = forms.MultipleChoiceField(choices=FAMILIA_CHOICES,label='Parentesco',required=False)
        self.fields['edad_inicio'] = forms.IntegerField(required=False,label='Edad inicio')
        self.fields['edad_fin'] = forms.IntegerField(required=False,label='Edad fin')


class SubfiltroProduccion(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SubfiltroProduccion, self).__init__(*args, **kwargs)
        self.fields['rubro'] = forms.ModelChoiceField(required=False,queryset=Cultivo.objects.all(),widget=forms.Select(attrs={
            'class': 'form-control',
            }))
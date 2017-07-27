# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from productores.forms import *
from django.http import HttpResponse
import json as simplejson
from django.db.models import Avg, Sum, F
import collections

# Create your views here.
@login_required
def index(request,template='frontend/index.html'):
	#afiliados
	total = Afiliado.objects.all().distinct().count()
	mujeres = Afiliado.objects.filter(sexo = 'Femenino').distinct().count()
	hombres = Afiliado.objects.filter(sexo = 'Masculino').distinct().count()

	return render(request, template, locals())

def _queryset_filtrado(request):
    params = {}

    if request.session['anio']:
        params['anio'] = request.session['anio']

    # if request.session['departamento']:
    #     params['afiliado__departamento__in'] = request.session['departamento']

    if request.session['municipio']:
        params['afiliado__municipio__in'] = request.session['municipio']

    if request.session['comunidad']:
        params['afiliado__comunidad__in'] = request.session['comunidad']

    if request.session['sexo']:
        params['afiliado__sexo'] = request.session['sexo']

    if request.session['edad_inicio'] and request.session['edad_fin']:
        params['afiliado__edad__range'] = (request.session['edad_inicio'],request.session['edad_fin'])

	unvalid_keys = []
	for key in params:
		if not params[key]:
			unvalid_keys.append(key)

	for key in unvalid_keys:
		del params[key]

    return Encuesta.objects.filter(**params)

@login_required
def consulta(request,template="frontend/consulta.html"):
    if request.method == 'POST':
        mensaje = None
        form = EncuestaForm(request.POST)
        if form.is_valid():
            request.session['anio'] = form.cleaned_data['anio']
            # request.session['departamento'] = form.cleaned_data['departamento']
            request.session['municipio'] = form.cleaned_data['municipio']
            request.session['comunidad'] = form.cleaned_data['comunidad']
            request.session['sexo'] = form.cleaned_data['sexo']
            request.session['edad_inicio'] = form.cleaned_data['edad_inicio']
            request.session['edad_fin'] = form.cleaned_data['edad_fin']

            mensaje = "Todas las variables estan correctamente :)"
            request.session['activo'] = True
            centinela = 1
        else:
            centinela = 0

    else:
        form = EncuestaForm()
        mensaje = "Existen alguno errores"
        try:
            del request.session['anio']
            # del request.session['departamento']
            del request.session['municipio']
            del request.session['communidad']
            del request.session['sexo']
            del request.session['edad_inicio']
            del request.session['edad_fin']
        except:
            pass

    return render(request, template, locals())

def datos_generales(request,template='frontend/datos_generales.html'):
	filtro = _queryset_filtrado(request)

	personas = filtro.count()

	escolaridad_mujer = {}
	total_mujeres = filtro.filter(afiliado__sexo = 'Femenino').count()
	for obj in ESCOLARIDAD_CHOICES:
		conteo = filtro.filter(escolaridad__escolaridad = obj[0],afiliado__sexo = 'Femenino').count()
		escolaridad_mujer[obj[0]] = conteo

	escolaridad_hombre = {}
	total_hombres = filtro.filter(afiliado__sexo = 'Masculino').count()
	for obj in ESCOLARIDAD_CHOICES:
		conteo = filtro.filter(escolaridad__escolaridad = obj[0],afiliado__sexo = 'Masculino').count()
		escolaridad_hombre[obj[0]] = conteo

	#miembros que dependen del jefe
	personas_dependen = {}
	for obj in PERSONAS_CHOICES:
		avg = filtro.filter(personasdependen__opcion = obj[0]).aggregate(avg = Avg('personasdependen__cantidad'))['avg']
		personas_dependen[obj[0]] = avg

	#hombre y mujeres emigran
	emigran_h = filtro.aggregate(total = Sum('familiaemigra__hombres'))['total']
	emigran_m = filtro.aggregate(total = Sum('familiaemigra__mujeres'))['total']

	#destino migrantes
	migran = {}
	for obj in EMIGRAN_CHOICES:
		conteo = filtro.filter(familiaemigra__donde_emigran = obj[0]).count()
		migran[obj[0]] = conteo

	#periodo de tiepo que migran
	periodo = {}
	for obj in TIEMPO_CHOICES:
		conteo = filtro.filter(familiaemigra__tiempo = obj[0]).count()
		periodo[obj[0]] = conteo

	#meses que migran
	meses = collections.OrderedDict()
	for obj in MESES_CHOICES:
		conteo = filtro.filter(familiaemigra__meses__contains = obj[0]).count()
		meses[obj[0]] = conteo

	return render(request, template, locals())

#ajax
def get_comunies(request):
    ids = request.GET.get('ids', '')
    dicc = {}
    resultado = []
    if ids:
        lista = ids.split(',')
        for id in lista:
            try:
                munici = Municipio.objects.get(id = id)
                comunidades = Comunidad.objects.filter(municipio__id = munici.id).order_by('nombre')
                lista1 = []
                for comunidad in comunidades:
                    comu = {}
                    comu['id'] = comunidad.id
                    comu['nombre'] = comunidad.nombre
                    lista1.append(comu)
                    dicc[munici.nombre] = lista1
            except:
                pass

    resultado.append(dicc)

    return HttpResponse(simplejson.dumps(resultado), content_type = 'application/json')

def saca_porcentajes(dato, total, formato=True):
	if dato != None:
		try:
			porcentaje = (dato/float(total)) * 100 if total != None or total != 0 else 0
		except:
			return 0
		if formato:
			return porcentaje
		else:
			return '%.2f' % porcentaje
	else:
		return 0
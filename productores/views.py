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

	#acceso internet
	internet = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(datosgenerales__acceso_internet = obj[0]).count()
		internet[obj[0]] = conteo

	#estado civil
	estado_civil = {}
	for obj in ESTADO_CIVIL_CHOICES:
		conteo = filtro.filter(datosgenerales__estado_civil = obj[0]).count()
		estado_civil[obj[0]] = conteo

	return render(request, template, locals())

def datos_familiares(request,template='frontend/datos_familiares.html'):
	filtro = _queryset_filtrado(request)

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

def datos_propiedad(request,template='frontend/datos_propiedad.html'):
	filtro = _queryset_filtrado(request)

	#areas
	areas_finca = {}
	list_areas = ['Pasto','Agrícola','Forestal','Café','Caña']
	for obj in Areas.objects.all():
		if obj.nombre in list_areas:
			areas = filtro.filter(areasfinca__areas = obj.id).aggregate(suma = Sum('areasfinca__mz'))['suma']
			areas_finca[obj] = areas
	try:
		otras_areas = filtro.aggregate(suma = Sum('areasfinca__mz'))['suma'].exclude(areasfinca__areas__in = list_areas)
		areas_finca['Otros'] = otras_areas
	except:
		areas_finca['Otros'] = 0

	#otras areas
	otras_areas_finca = {}
	list_areas = ['Pasto','Agrícola','Forestal','Café','Caña']
	for obj in Areas.objects.all():
		if obj.nombre in list_areas:
			areas = filtro.filter(otrastierras__areas = obj.id).aggregate(suma = Sum('otrastierras__mz'))['suma']
			otras_areas_finca[obj] = areas
	try:
		otras_areas = filtro.aggregate(suma = Sum('otrastierras__mz'))['suma'].exclude(otrastierras__areas__in = list_areas)
		otras_areas_finca['Otros'] = otras_areas
	except:
		otras_areas_finca['Otros'] = 0

	#origen propiedad
	propiedad = {}
	list_origen = ['Comprada','Herencia','Reforma Agraria','Alquilada']
	for obj in Origen.objects.all():
		if obj.nombre in list_origen:
			conteo = filtro.filter(origenpropiedad__opcion = obj.id).count()
			propiedad[obj] = conteo
	try:
		otros_origen = filtro.count().exclude(origenpropiedad__opcion__in = list_origen)
		propiedad['Otros'] = otros_origen
	except:
		propiedad['Otros'] = 0

	#tenencia 
	tenencia = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(formatenencia__legalizada = obj[0]).count()
		tenencia[obj[0]] = conteo

	#documento propiedad
	doc_propiedad = {}
	list_doc = ['Constancia de asignación','Titulo supletorio','Titulo de Reforma agraria','Escritura pública']
	for obj in Documento.objects.all():
		if obj.nombre in list_doc:
			conteo = filtro.filter(documentopropiedad__documento = obj.id).count()
			doc_propiedad[obj] = conteo
	try:
		otros_doc = filtro.count().exclude(documentopropiedad__documento__in = list_doc)
		doc_propiedad['Otros'] = otros_doc
	except:
		doc_propiedad['Otros'] = 0

	#acceso agua
	encuestados = filtro.count()
	acceso_agua = {}
	list_agua = ['Ojo de Agua','Pozo','Quebrada','Agua potable/Acueducto','Río']
	for obj in Sistema.objects.all():
		if obj.nombre in list_agua:
			conteo = filtro.filter(sistemaagua__sistema = obj.id).count()
			acceso_agua[obj] = conteo,saca_porcentajes(conteo,encuestados,False)
	try:
		otros_agua = filtro.count().exclude(sistemaagua__sistema__in = list_agua)
		acceso_agua['Otros'] = otros_agua,saca_porcentajes(otros_agua,encuestados,False)
	except:
		acceso_agua['Otros'] = 0

	#energia 
	energia = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(energiaelectrica__respuesta = obj[0]).count()
		energia[obj[0]] = conteo

	#contrata mano obra
	mano_obra = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(manoobra__mano_obra = obj[0]).count()
		mano_obra[obj[0]] = conteo

	#contratacion
	list_contratacion = []
	rubro = filtro.values_list('tablaempleo__rubro__nombre',flat=True).distinct()
	for obj in rubro:
		cont = filtro.filter(tablaempleo__rubro__nombre = obj).aggregate(
				temporal_hombres = Sum('tablaempleo__temporal_hombres'),
				temporal_mujeres = Sum('tablaempleo__temporal_mujeres'),
				permanente_hombres = Sum('tablaempleo__permanente_hombres'),
				permanente_mujeres = Sum('tablaempleo__permanente_mujeres'),
				familiar_hombres = Sum('tablaempleo__familiar_hombres'),
				familiar_mujeres = Sum('tablaempleo__familiar_mujeres'))

		list_contratacion.append((obj,cont['temporal_hombres'],cont['temporal_mujeres'],
									cont['permanente_hombres'],cont['permanente_mujeres'],
									cont['familiar_hombres'],cont['familiar_mujeres']))

	#infraestructura
	infra = {}
	list_infra = ['Troja','Gallinero','Corral','Chiquero','Edificio de café','Horno','Letrina',
					'Pilas para agua']
	for obj in Infraestructuras.objects.all():
		if obj.nombre in list_infra:
			conteo = filtro.filter(infraestructura__tipo = obj.id,infraestructura__possee = 'Si').count()
			infra[obj] = conteo
	try:
		otros_infra = filtro.count().exclude(infraestructura__tipo__in = list_infra,infraestructura__possee = 'Si')
		infra['Otros'] = otros_infra
	except:
		infra['Otros'] = 0

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
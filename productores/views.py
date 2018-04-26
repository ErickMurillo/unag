# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from productores.forms import *
from django.http import HttpResponse, HttpResponseRedirect
import json as simplejson
from django.db.models import Avg, Sum, F, Count,Q
import collections

# Create your views here.
SI_NO_CHOICES = (('Si','Si'), ('No','No'))

@login_required
def index(request,template='frontend/index.html'):
	RONDA_CHOICES = ((1,'I'),(2,'II'), (3,'III'), 
					(4,'IV'),(5,'V')
				)

	#afiliados
	total_afiliados = Afiliado.objects.all().distinct().count()
	mujeres_total = Afiliado.objects.filter(sexo = 'Femenino').distinct().count()
	hombres_total = Afiliado.objects.filter(sexo = 'Masculino').distinct().count()

	#departamentos
	muni = Encuesta.objects.order_by('afiliado__municipio').distinct().values_list('afiliado__municipio__id', flat=True)
	deptos = Municipio.objects.filter(id = muni).values_list('departamento__id','departamento__nombre').distinct()

	years = []
	for en in Encuesta.objects.order_by('ronda').values_list('ronda', flat=True):
		years.append(en)
	anios = list(sorted(set(years)))

	lista_ronda = []
	for r in RONDA_CHOICES:
		if r[0] in anios:
			list_anios = []
			for a in Encuesta.objects.filter(ronda = r[0]).values_list('anio', flat=True):
				list_anios.append(a)

			lista = list(sorted(set(list_anios)))
			lista_ronda.append((r[0],'Ronda ' + r[1] + ' ('+str(lista[0])+'-'+str(lista[-1])+')'))

	#-------------------------
	dic_anios = collections.OrderedDict()
	for anio in lista_ronda:
		#areas
		if request.GET.get('departamento') and request.GET.get('departamento') != 'all':
			dep = int(request.GET['departamento'])
			dic_areas = {}
			for obj in Areas.objects.all():
				areas = AreasFinca.objects.filter(encuesta__afiliado__municipio__departamento = dep,areas = obj,encuesta__ronda = anio[0]).aggregate(total = Sum('mz'))['total']
				if areas == None:
					areas = 0

				conteo_prod = AreasFinca.objects.filter(encuesta__afiliado__municipio__departamento = dep,areas = obj,encuesta__ronda = anio[0]).distinct('id')
				l = []
				for x in conteo_prod:
					l.append(x.id)

				otras_areas = OtrasTierras.objects.filter(encuesta__afiliado__municipio__departamento = dep,areas = obj,encuesta__ronda = anio[0]).aggregate(total = Sum('mz'))['total']
				if otras_areas == None:
					otras_areas = 0

				conteo_prod2 = OtrasTierras.objects.filter(encuesta__afiliado__municipio__departamento = dep,areas = obj,encuesta__ronda = anio[0]).distinct('id')
				l2 = []
				for x in conteo_prod2:
					l2.append(x.id)

				#hombres
				hombres_areas = AreasFinca.objects.filter(encuesta__afiliado__municipio__departamento = dep,encuesta__afiliado__sexo = 'Masculino',areas = obj,encuesta__ronda = anio[0]).aggregate(total = Sum('mz'))['total']
				if hombres_areas == None:
					hombres_areas = 0

				hombres_otras_areas = OtrasTierras.objects.filter(encuesta__afiliado__municipio__departamento = dep,encuesta__afiliado__sexo = 'Masculino',areas = obj,encuesta__ronda = anio[0]).aggregate(total = Sum('mz'))['total']
				if hombres_otras_areas == None:
					hombres_otras_areas = 0

				#mujeres
				mujeres_areas = AreasFinca.objects.filter(encuesta__afiliado__municipio__departamento = dep,encuesta__afiliado__sexo = 'Femenino',areas = obj,encuesta__ronda = anio[0]).aggregate(total = Sum('mz'))['total']
				if mujeres_areas == None:
					mujeres_areas = 0

				mujeres_otras_areas = OtrasTierras.objects.filter(encuesta__afiliado__municipio__departamento = dep,encuesta__afiliado__sexo = 'Femenino',areas = obj,encuesta__ronda = anio[0]).aggregate(total = Sum('mz'))['total']
				if mujeres_otras_areas == None:
					mujeres_otras_areas = 0

				#totales				
				result = l + l2
				result = list(sorted(set(result)))
				conteo = len(result)
				
				total = areas + otras_areas
				hombres = hombres_areas + hombres_otras_areas
				porcentaje_h = saca_porcentajes(hombres,total,False)
				mujeres = mujeres_areas + mujeres_otras_areas
				porcentaje_m = saca_porcentajes(mujeres,total,False)
				dic_areas[obj] = (total,conteo,hombres,porcentaje_h,mujeres,porcentaje_m)
		else:
			dic_areas = {}
			for obj in Areas.objects.exclude(nombre__in = ['Piscicultura/Acuícola','Apícola']):
				areas = AreasFinca.objects.filter(areas = obj,encuesta__ronda = anio[0]).aggregate(total = Sum('mz'))['total']
				if areas == None:
					areas = 0

				conteo_prod = AreasFinca.objects.filter(areas = obj,encuesta__ronda = anio[0]).distinct('id')
				l = []
				for x in conteo_prod:
					l.append(x.id)

				otras_areas = OtrasTierras.objects.filter(areas = obj,encuesta__ronda = anio[0]).aggregate(total = Sum('mz'))['total']
				if otras_areas == None:
					otras_areas = 0

				conteo_prod2 = OtrasTierras.objects.filter(areas = obj,encuesta__ronda = anio[0]).distinct('id')
				l2 = []
				for x in conteo_prod2:
					l2.append(x.id)

				#hombres
				hombres_areas = AreasFinca.objects.filter(encuesta__afiliado__sexo = 'Masculino',areas = obj,encuesta__ronda = anio[0]).aggregate(total = Sum('mz'))['total']
				if hombres_areas == None:
					hombres_areas = 0

				hombres_otras_areas = OtrasTierras.objects.filter(encuesta__afiliado__sexo = 'Masculino',areas = obj,encuesta__ronda = anio[0]).aggregate(total = Sum('mz'))['total']
				if hombres_otras_areas == None:
					hombres_otras_areas = 0

				#mujeres
				mujeres_areas = AreasFinca.objects.filter(encuesta__afiliado__sexo = 'Femenino',areas = obj,encuesta__ronda = anio[0]).aggregate(total = Sum('mz'))['total']
				if mujeres_areas == None:
					mujeres_areas = 0

				mujeres_otras_areas = OtrasTierras.objects.filter(encuesta__afiliado__sexo = 'Femenino',areas = obj,encuesta__ronda = anio[0]).aggregate(total = Sum('mz'))['total']
				if mujeres_otras_areas == None:
					mujeres_otras_areas = 0

				#totales				
				result = l + l2
				result = list(sorted(set(result)))
				conteo = len(result)
				
				total = areas + otras_areas
				hombres = hombres_areas + hombres_otras_areas
				porcentaje_h = saca_porcentajes(hombres,total,False)
				mujeres = mujeres_areas + mujeres_otras_areas
				porcentaje_m = saca_porcentajes(mujeres,total,False)

				dic_areas[obj] = (total,conteo,hombres,porcentaje_h,mujeres,porcentaje_m)

		#rubros por departamento
		if request.GET.get('departamento-rubros') and request.GET.get('departamento-rubros') != 'all':
			dep2 = int(request.GET['departamento-rubros'])			
			dict = {}
			for obj in Cultivo.objects.all():
				sumatoria = Agricultura.objects.filter(rubro = obj,encuesta__ronda = anio[0],
											encuesta__afiliado__municipio__departamento = dep2).aggregate(
										area = Sum('area_sembrada'),produccion = Sum('produccion_total'))
				dict[obj] = (sumatoria['area'],sumatoria['produccion'])

			d = collections.Counter(dict)
			d.most_common()
			rubros = {}
			for k, v in d.most_common(5):
				rubros[k] = v[0],v[1]
		else:
			dict = {}
			for obj in Cultivo.objects.all():
				sumatoria = Agricultura.objects.filter(rubro = obj,encuesta__ronda = anio[0]).aggregate(
										area = Sum('area_sembrada'),produccion = Sum('produccion_total'))
				dict[obj] = (sumatoria['area'],sumatoria['produccion'])

			d = collections.Counter(dict)
			d.most_common()
			rubros = {}
			for k, v in d.most_common(5):
				rubros[k] = v[0],v[1]

		dic_anios[anio[0],anio[1]] = dic_areas,rubros

	#miembros por depto y municipio
	list_deptos = []
	list_muni = []
	for obj in Afiliado.objects.all():
		list_deptos.append(obj.municipio.departamento)
	deptos = list(sorted(set(list_deptos)))

	dic_deptos = {}
	for x in deptos:
		afiliados = Afiliado.objects.filter(municipio__departamento__nombre = x)
		municipios = afiliados.values_list('municipio__nombre',flat=True).distinct()
		conteo = afiliados.count()
		list_munis = []
		for obj in municipios:
			conteo_munis = afiliados.filter(municipio__nombre = obj).count()
			list_munis.append((obj,conteo_munis))
		dic_deptos[x] = conteo,list_munis

	return render(request, template, locals())

def _queryset_filtrado_afiliado(request):
	params = {}

	if request.session['nombre']:
		params['nombre'] = request.session['nombre']

	unvalid_keys = []
	for key in params:
		if not params[key]:
			unvalid_keys.append(key)

	for key in unvalid_keys:
		del params[key]

	return Afiliado.objects.filter(**params)

@login_required
def afiliados(request,template='frontend/afiliados.html'):
	if request.method == 'POST':
		mensaje = None
		form = AfiliadoForm(request.POST)
		if form.is_valid():
			request.session['nombre'] = form.cleaned_data['nombre']

			mensaje = "Todas las variables estan correctamente :)"
			request.session['activo'] = True
			centinela = 1

			return HttpResponseRedirect('/afiliados/datos-personales/')
		else:
			centinela = 0

	else:
		form = AfiliadoForm()
		mensaje = "Existen alguno errores"
		try:
			del request.session['nombre']
		except:
			pass

	return render(request, template, locals())

@login_required
def afiliados_personales(request,template="frontend/afiliados_personales.html"):
	if request.method == 'POST':
		mensaje = None
		form = AfiliadoForm(request.POST)
		if form.is_valid():
			request.session['nombre'] = form.cleaned_data['nombre']

			mensaje = "Todas las variables estan correctamente :)"
			request.session['activo'] = True
			centinela = 1
		else:
			centinela = 0
	else:
		form = AfiliadoForm()
		mensaje = "Existen alguno errores"

	filtro = _queryset_filtrado_afiliado(request)

	id = filtro[0].id
	afiliado = Afiliado.objects.get(id = id)
	escolaridad = Escolaridad.objects.filter(encuesta__afiliado = id).values_list('escolaridad',flat=True).last()

	anios_encuesta = Encuesta.objects.filter(afiliado = afiliado.id).values_list('anio',flat=True)
	estado_civil = Encuesta.objects.filter(afiliado = afiliado.id).values_list('datosgenerales__estado_civil', flat=True).last()
	acceso_internet = Encuesta.objects.filter(afiliado = afiliado.id).values_list('datosgenerales__acceso_internet', flat=True).last()

	return render(request, template, locals())

@login_required
def afiliados_familiares(request,template="frontend/afiliados_familiares.html"):
	if request.method == 'POST':
		mensaje = None
		form = AfiliadoForm(request.POST)
		if form.is_valid():
			request.session['nombre'] = form.cleaned_data['nombre']

			mensaje = "Todas las variables estan correctamente :)"
			request.session['activo'] = True
			centinela = 1
		else:
			centinela = 0
	else:
		form = AfiliadoForm()
		mensaje = "Existen alguno errores"

	filtro = _queryset_filtrado_afiliado(request)

	id = filtro[0].id
	
	afiliado = Afiliado.objects.get(id = id)
	anios_encuesta = Encuesta.objects.filter(afiliado = afiliado.id).values_list('anio',flat=True)

	years = collections.OrderedDict()
	for anio in anios_encuesta:
		#dependen
		hombres = PersonasDependen.objects.filter(encuesta__afiliado = id,opcion = 'Adultos: Hombres',encuesta__anio = anio).aggregate(total= Sum('cantidad'))['total']
		mujeres = PersonasDependen.objects.filter(encuesta__afiliado = id,opcion = 'Adultos: Mujeres',encuesta__anio = anio).aggregate(total= Sum('cantidad'))['total']
		ninas = PersonasDependen.objects.filter(encuesta__afiliado = id,opcion = 'Niñas menores de 12 años',encuesta__anio = anio).aggregate(total= Sum('cantidad'))['total']
		ninos = PersonasDependen.objects.filter(encuesta__afiliado = id,opcion = 'Niños menores de 12 años',encuesta__anio = anio).aggregate(total= Sum('cantidad'))['total']

		familiares = []
		for x in DatosFamiliares.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id):
			familiares.append((x.nombres,x.sexo,x.edad,x.escolaridad,x.parentesco,x.donde_emigran,
								x.tiempo,x.meses))


		emigran = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list(
					'familiaemigra__hombres',
					'familiaemigra__mujeres')

		# hombres_emigran = DatosFamiliares.objects.filter(encuesta__anio = anio,donde_emigran__isnull = False,
		# 					encuesta__afiliado = afiliado.id,sexo = "Masculino").count()
		hombres_emigran = FamiliaEmigra.objects.filter(encuesta__anio = anio,
							encuesta__afiliado = afiliado.id).values_list('hombres',flat = True)


		# mujeres_emigran = DatosFamiliares.objects.filter(encuesta__anio = anio,donde_emigran__isnull = False,
		# 					encuesta__afiliado = afiliado.id,sexo = "Femenino").count()
		mujeres_emigran = FamiliaEmigra.objects.filter(encuesta__anio = anio,
							encuesta__afiliado = afiliado.id).values_list('mujeres',flat = True)

		years[anio] = (hombres,mujeres,ninas,ninos,familiares,hombres_emigran,mujeres_emigran)

	return render(request, template, locals())

@login_required
def afiliados_propiedad(request,template="frontend/afiliados_propiedad.html"):
	if request.method == 'POST':
		mensaje = None
		form = AfiliadoForm(request.POST)
		if form.is_valid():
			request.session['nombre'] = form.cleaned_data['nombre']

			mensaje = "Todas las variables estan correctamente :)"
			request.session['activo'] = True
			centinela = 1
		else:
			centinela = 0
	else:
		form = AfiliadoForm()
		mensaje = "Existen alguno errores"

	filtro = _queryset_filtrado_afiliado(request)

	id = filtro[0].id
	
	afiliado = Afiliado.objects.get(id = id)
	anios_encuesta = Encuesta.objects.filter(afiliado = afiliado.id).values_list('anio',flat=True)

	years = collections.OrderedDict()
	for anio in anios_encuesta:
		areas = {}
		otras = {}
		for obj in Areas.objects.all():
			areas_finca = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,areasfinca__areas = obj).values_list(
					'areasfinca__mz',flat=True)
			areas[obj] = areas_finca

			otras_areas = Encuesta.objects.filter(tierrasalquiladas__posse = 'Si',anio = anio,
							afiliado = afiliado.id,otrastierras__areas = obj).values_list(
							'otrastierras__mz',flat=True)
			otras[obj] = otras_areas

		total_finca = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list(
					'areasfinca__mz',flat=True)
		total_otras_areas = Encuesta.objects.filter(tierrasalquiladas__posse = 'Si',anio = anio,
							afiliado = afiliado.id).values_list(
							'otrastierras__mz',flat=True)

		legalizada = FormaTenencia.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('legalizada',flat=True)
		documento = DocumentoPropiedad.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('documento__nombre',flat=True)
		agua = SistemaAgua.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('sistema__nombre',flat=True)
		energia = EnergiaElectrica.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('respuesta',flat=True)
		mano_obra = ManoObra.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('mano_obra',flat=True)
		pisci = Acuicola.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('posse',flat=True)
		colmenas = Apicola.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('colmenas',flat=True)

		tabla_empleo = []
		empleo = TablaEmpleo.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id)
		rubro = empleo.values_list('rubro__nombre',flat=True).distinct()
		for obj in rubro:
			cont = empleo.filter(rubro__nombre = obj).aggregate(
					temporal_hombres = Sum('temporal_hombres'),
					temporal_mujeres = Sum('temporal_mujeres'),
					permanente_hombres = Sum('permanente_hombres'),
					permanente_mujeres = Sum('permanente_mujeres'),
					familiar_hombres = Sum('familiar_hombres'),
					familiar_mujeres = Sum('familiar_mujeres'))

			tabla_empleo.append((obj,cont['temporal_hombres'],cont['temporal_mujeres'],
										cont['permanente_hombres'],cont['permanente_mujeres'],
										cont['familiar_hombres'],cont['familiar_mujeres']))

		infraestructura = Infraestructura.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('tipo__nombre',flat=True)

		years[anio] = (areas,otras,legalizada,documento,agua,energia,mano_obra,tabla_empleo,infraestructura,pisci,colmenas,
			total_finca,total_otras_areas)

	return render(request, template, locals())

@login_required
def afiliados_produccion(request,template="frontend/afiliados_produccion.html"):
	if request.method == 'POST':
		mensaje = None
		form = AfiliadoForm(request.POST)
		if form.is_valid():
			request.session['nombre'] = form.cleaned_data['nombre']

			mensaje = "Todas las variables estan correctamente :)"
			request.session['activo'] = True
			centinela = 1
		else:
			centinela = 0
	else:
		form = AfiliadoForm()
		mensaje = "Existen alguno errores"

	filtro = _queryset_filtrado_afiliado(request)

	id = filtro[0].id
	
	afiliado = Afiliado.objects.get(id = id)
	anios_encuesta = Encuesta.objects.filter(afiliado = afiliado.id).values_list('anio',flat=True)

	years = collections.OrderedDict()
	for anio in anios_encuesta:
		#agricultura
		#primera
		primera = []
		cultivos_primera = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Cultivo de primera').values_list('agricultura__rubro',flat=True)
		for x in PRODUCCION_CHOICES2:
			for obj in Cultivo.objects.filter(id__in = cultivos_primera):
				cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj,agricultura__tipo = 'Cultivo de primera',agricultura__quien_vende = x[0]).aggregate(
							area_sembrada = Sum('agricultura__area_sembrada'),
							produccion_total = Sum('agricultura__produccion_total'),
							semillas = Sum('agricultura__semillas'),
							consumo_humano = Sum('agricultura__consumo_humano'),
							consumo_animal = Sum('agricultura__consumo_animal'),
							venta = Sum('agricultura__venta'),
							costo_produccion = Avg('agricultura__costo_produccion'),
							ingresos_produccion = Avg('agricultura__ingresos_produccion'),
							ganancia_perdida = Avg('agricultura__ganancia_perdida')) 

				if cultivo['area_sembrada'] != None:
					primera.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
									cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
									cultivo['venta'],x[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
									cultivo['ganancia_perdida']))
		primera.sort()


		#postrera
		postrera = []
		cultivos_postrera = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Cultivo de postrera').values_list('agricultura__rubro',flat=True)
		for x in PRODUCCION_CHOICES2:
			for obj in Cultivo.objects.filter(id__in = cultivos_postrera):
				cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj,agricultura__tipo = 'Cultivo de postrera',agricultura__quien_vende = x[0]).aggregate(
							area_sembrada = Sum('agricultura__area_sembrada'),
							produccion_total = Sum('agricultura__produccion_total'),
							semillas = Sum('agricultura__semillas'),
							consumo_humano = Sum('agricultura__consumo_humano'),
							consumo_animal = Sum('agricultura__consumo_animal'),
							venta = Sum('agricultura__venta'),
							costo_produccion = Avg('agricultura__costo_produccion'),
							ingresos_produccion = Avg('agricultura__ingresos_produccion'),
							ganancia_perdida = Avg('agricultura__ganancia_perdida'))

				if cultivo['area_sembrada'] != None:
					postrera.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
									cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
									cultivo['venta'],x[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
									cultivo['ganancia_perdida']))
		postrera.sort()

		#apante
		apante = []
		cultivos_apante = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Cultivo de apante').values_list('agricultura__rubro',flat=True)
		for x in PRODUCCION_CHOICES2:
			for obj in Cultivo.objects.filter(id__in = cultivos_apante):
				cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj,agricultura__tipo = 'Cultivo de apante',agricultura__quien_vende = x[0]).aggregate(
							area_sembrada = Sum('agricultura__area_sembrada'),
							produccion_total = Sum('agricultura__produccion_total'),
							semillas = Sum('agricultura__semillas'),
							consumo_humano = Sum('agricultura__consumo_humano'),
							consumo_animal = Sum('agricultura__consumo_animal'),
							venta = Sum('agricultura__venta'),
							costo_produccion = Avg('agricultura__costo_produccion'),
							ingresos_produccion = Avg('agricultura__ingresos_produccion'),
							ganancia_perdida = Avg('agricultura__ganancia_perdida'))
				
				if cultivo['area_sembrada'] != None:
					apante.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
									cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
									cultivo['venta'],x[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
									cultivo['ganancia_perdida']))
		apante.sort()

		#permanentes
		permanentes = []
		cultivos_permanentes = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Cultivos permanentes (Frutales, Cítricos, …)').values_list('agricultura__rubro',flat=True)
		for x in PRODUCCION_CHOICES2:
			for obj in Cultivo.objects.filter(id__in = cultivos_permanentes):
				cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj,agricultura__tipo = 'Cultivos permanentes (Frutales, Cítricos, …)',agricultura__quien_vende = x[0]).aggregate(
							area_sembrada = Sum('agricultura__area_sembrada'),
							produccion_total = Sum('agricultura__produccion_total'),
							semillas = Sum('agricultura__semillas'),
							consumo_humano = Sum('agricultura__consumo_humano'),
							consumo_animal = Sum('agricultura__consumo_animal'),
							venta = Sum('agricultura__venta'),
							costo_produccion = Avg('agricultura__costo_produccion'),
							ingresos_produccion = Avg('agricultura__ingresos_produccion'),
							ganancia_perdida = Avg('agricultura__ganancia_perdida'))
				
				if cultivo['area_sembrada'] != None:
					permanentes.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
									cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
									cultivo['venta'],x[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
									cultivo['ganancia_perdida']))
		permanentes.sort()

		#otros
		otros = []
		cultivos_otros = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Otros').values_list('agricultura__rubro',flat=True)
		for x in PRODUCCION_CHOICES2:
			for obj in Cultivo.objects.filter(id__in = cultivos_otros):
				cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj,agricultura__tipo = 'Otros',agricultura__quien_vende = x[0]).aggregate(
							area_sembrada = Sum('agricultura__area_sembrada'),
							produccion_total = Sum('agricultura__produccion_total'),
							semillas = Sum('agricultura__semillas'),
							consumo_humano = Sum('agricultura__consumo_humano'),
							consumo_animal = Sum('agricultura__consumo_animal'),
							venta = Sum('agricultura__venta'),
							costo_produccion = Avg('agricultura__costo_produccion'),
							ingresos_produccion = Avg('agricultura__ingresos_produccion'),
							ganancia_perdida = Avg('agricultura__ganancia_perdida'))
				
				if cultivo['area_sembrada'] != None:
					otros.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
									cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
									cultivo['venta'],x[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
									cultivo['ganancia_perdida']))
		otros.sort()

		#inventario animales
		animales = []
		for animal in Animales.objects.all():
			conteos = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,inventarioanimales__animal = animal).aggregate(
									cantidad = Sum('inventarioanimales__cantidad'),
									cuanto_vende = Sum('inventarioanimales__cuanto_vende'))

			animales.append((animal,conteos['cantidad'],conteos['cuanto_vende']))

		#produccion leche y huevos
		produccion = {}
		for obj in PRODUCCION_CHOICES:
			list_prod = []
			for x in QUIEN_VENDE_CHOICES:
				conteos = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,produccionhuevosleche__tipo_produccion = obj[0],produccionhuevosleche__quien_vende = x[0]).aggregate(
										cantidad = Sum('produccionhuevosleche__cantidad'),
										cuanto_vende = Sum('produccionhuevosleche__cuanto_vende'))

				list_prod.append((x[0],conteos['cantidad'],conteos['cuanto_vende']))
			produccion[obj[0]] = list_prod

		years[anio] = (primera,postrera,apante,permanentes,otros,animales,produccion)

	return render(request, template, locals())

@login_required
def afiliados_organizacion(request,template="frontend/afiliados_organizacion.html"):
	if request.method == 'POST':
		mensaje = None
		form = AfiliadoForm(request.POST)
		if form.is_valid():
			request.session['nombre'] = form.cleaned_data['nombre']

			mensaje = "Todas las variables estan correctamente :)"
			request.session['activo'] = True
			centinela = 1
		else:
			centinela = 0
	else:
		form = AfiliadoForm()
		mensaje = "Existen alguno errores"

	filtro = _queryset_filtrado_afiliado(request)

	id = filtro[0].id
	
	afiliado = Afiliado.objects.get(id = id)
	anios_encuesta = Encuesta.objects.filter(afiliado = afiliado.id).values_list('anio',flat=True)

	years = collections.OrderedDict()
	for anio in anios_encuesta:
		cotiza = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('cotizacion__respuesta',flat=True)
		si_cotiza = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list(
						'respuestasicotiza__donde_cotiza__nombre','respuestasicotiza__desde_cuando',
						'respuestasicotiza__cuanto_cotiza','respuestasicotiza__frecuencia')

		cooperativa = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('miembrocooperativa__respuesta',flat=True)
		list_cooperativas = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('miembrocooperativa__cooperativa__nombre',flat=True)

		proyecto = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('beneficiadoproyecto__respuesta',flat=True)
		list_proyectos = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('beneficiadoproyecto__proyectos__nombre',flat=True)

		credito = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('credito__respuesta','credito__proyectos__nombre')
		list_credito = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('credito__formas_recibe_credito__nombre',flat=True)

		problemas = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('cotizacionorganizacion__problemas_productor__nombre',flat=True)

		acciones = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('cotizacionorganizacion__acciones_cambio_climatico__nombre',flat=True)

		motivos_afiliacion = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('cotizacionorganizacion__afiliacion_unag__nombre',flat=True)

		comentarios = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('cotizacionorganizacion__comentarios',flat=True)

		years[anio] = (cotiza,si_cotiza,cooperativa,list_cooperativas,
						proyecto,list_proyectos,credito,list_credito,problemas,acciones,motivos_afiliacion,
						comentarios)

	return render(request, template, locals())

def _queryset_filtrado(request):
	params = {}

	if request.session['anio']:
		params['ronda'] = request.session['anio']

	if request.session['departamento']:
	    params['afiliado__municipio__departamento__in'] = request.session['departamento']

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
			#obtener label choice form
			for val in form.fields['anio'].choices:
				if int(val[0]) == int(form.cleaned_data['anio']):
					request.session['ronda'] = val[1]
					break
			#---------

			request.session['anio'] = form.cleaned_data['anio']
			request.session['departamento'] = form.cleaned_data['departamento']
			request.session['municipio'] = form.cleaned_data['municipio']
			request.session['comunidad'] = form.cleaned_data['comunidad']
			request.session['sexo'] = form.cleaned_data['sexo']
			request.session['edad_inicio'] = form.cleaned_data['edad_inicio']
			request.session['edad_fin'] = form.cleaned_data['edad_fin']

			mensaje = "Todas las variables estan correctamente :)"
			request.session['activo'] = True
			centinela = 1
			filtro = _queryset_filtrado(request)
			conteo_encuesta = filtro.count()
		else:
			centinela = 0

	else:
		form = EncuestaForm()
		mensaje = "Existen alguno errores"
		try:
			del request.session['anio']
			del request.session['ronda']
			del request.session['departamento']
			del request.session['municipio']
			del request.session['communidad']
			del request.session['sexo']
			del request.session['edad_inicio']
			del request.session['edad_fin']
		except:
			pass

	return render(request, template, locals())

@login_required
def datos_generales(request,template='frontend/datos_generales.html'):
	filtro = _queryset_filtrado(request)
	conteo_encuesta = filtro.count()

	personas = filtro.count()

	escolaridad_mujer = {}
	total_mujeres = filtro.filter(afiliado__sexo = 'Femenino').count()
	for obj in ESCOLARIDAD_CHOICES:
		conteo = filtro.filter(escolaridad__nivel_escolaridad = obj[0],escolaridad__escolaridad = 'Si',afiliado__sexo = 'Femenino').count()
		escolaridad_mujer[obj[0]] = conteo

	escolaridad_hombre = {}
	total_hombres = filtro.filter(afiliado__sexo = 'Masculino').count()
	for obj in ESCOLARIDAD_CHOICES:
		conteo = filtro.filter(escolaridad__nivel_escolaridad = obj[0],escolaridad__escolaridad = 'Si',afiliado__sexo = 'Masculino').count()
		escolaridad_hombre[obj[0]] = conteo

	#miembros que dependen del jefe
	personas_dependen = {}
	for obj in PERSONAS_CHOICES:
		conteo = filtro.filter(personasdependen__opcion = obj[0]).aggregate(sum = Sum('personasdependen__cantidad'))['sum']
		personas_dependen[obj[0]] = conteo

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

@login_required
def datos_familiares(request,template='frontend/datos_familiares.html'):
	filtro = _queryset_filtrado(request)
	conteo_encuesta = filtro.count()

	#hombre y mujeres emigran
	emigran_h = filtro.aggregate(total = Sum('familiaemigra__hombres'))['total']
	emigran_m = filtro.aggregate(total = Sum('familiaemigra__mujeres'))['total']

	#destino migrantes
	migran = {}
	for obj in EMIGRAN_CHOICES:
		conteo = filtro.filter(datosfamiliares__donde_emigran = obj[0]).count()
		migran[obj[0]] = conteo

	#periodo de tiepo que migran
	periodo = collections.OrderedDict()
	for obj in TIEMPO_CHOICES:
		conteo = filtro.filter(datosfamiliares__tiempo = obj[0]).count()
		periodo[obj[0]] = conteo

	#meses que migran
	meses = collections.OrderedDict()
	for obj in MESES_CHOICES:
		conteo = filtro.filter(datosfamiliares__meses__contains = obj[0]).count()
		meses[obj[0]] = conteo

	return render(request, template, locals())

@login_required
def datos_propiedad(request,template='frontend/datos_propiedad.html'):
	filtro = _queryset_filtrado(request)
	conteo_encuesta = filtro.count()

	#areas
	areas_finca = {}
	list_areas = filtro.values_list('areasfinca__areas',flat=True)
	list_origen = filtro.values_list('areasfinca__origen',flat=True)
	for obj in Areas.objects.filter(id__in = list_areas):
		areas = filtro.filter(areasfinca__areas = obj.id).aggregate(suma = Sum('areasfinca__mz'))['suma']
		# origen
		origen_prop = collections.OrderedDict()
		for x in Origen.objects.filter(id__in = list_origen):
			origen = filtro.filter(areasfinca__origen = x,areasfinca__areas = obj).count()
			origen_prop[x] = origen
		areas_finca[obj] = (areas,origen_prop)

	#otras areas
	otras_areas_finca = {}
	otras_areas = filtro.filter(tierrasalquiladas__posse = 'Si').values_list('otrastierras__areas',flat=True)
	for obj in Areas.objects.filter(id__in = otras_areas):
		areas = filtro.filter(otrastierras__areas = obj.id,tierrasalquiladas__posse = 'Si').aggregate(suma = Sum('otrastierras__mz'))['suma']
		otras_areas_finca[obj] = areas

	#tenencia
	tenencia = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(formatenencia__legalizada = obj[0]).count()
		tenencia[obj[0]] = conteo

	#documento propiedad
	doc_propiedad = {}
	list_doc = filtro.values_list('documentopropiedad__documento',flat=True)
	for obj in Documento.objects.filter(id__in = list_doc):
		conteo = filtro.filter(documentopropiedad__documento = obj.id).count()
		doc_propiedad[obj] = conteo

	#acceso agua
	encuestados = filtro.count()
	acceso_agua = {}
	list_agua = filtro.values_list('sistemaagua__sistema',flat=True)
	for obj in Sistema.objects.filter(id__in = list_agua):
		conteo = filtro.filter(sistemaagua__sistema = obj.id).count()
		acceso_agua[obj] = conteo,saca_porcentajes(conteo,encuestados,False)

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
		if obj != None:
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
	list_infra = filtro.values_list('infraestructura__tipo',flat=True)
	for obj in Infraestructuras.objects.filter(id__in = list_infra):
		conteo = filtro.filter(infraestructura__tipo = obj.id).count()
		infra[obj] = conteo

	# piscicultura
	pisci = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(acuicola__posse = obj[0]).count()
		pisci[obj[1]] = conteo

	#colmenas
	total_colmenas = filtro.aggregate(total = Sum('apicola__colmenas'))['total']
	prom_colmenas = filtro.aggregate(total = Avg('apicola__colmenas'))['total']

	return render(request, template, locals())

@login_required
def datos_produccion(request,template='frontend/datos_produccion.html'):
	filtro = _queryset_filtrado(request)
	encuestados = filtro.count()
	conteo_encuesta = filtro.count()

	dict = {}
	for obj in Cultivo.objects.all():
		sumatoria = filtro.filter(agricultura__rubro = obj).aggregate(
								area = Sum('agricultura__area_sembrada'),produccion = Sum('agricultura__produccion_total'))
		dict[obj] = (sumatoria['area'],sumatoria['produccion'])

	d = collections.Counter(dict)
	d.most_common()
	rubros = {}
	for k, v in d.most_common(5):
		rubros[k] = v[0],v[1]

	#inventario animales
	animales = []
	for animal in Animales.objects.all():
		conteos = filtro.filter(inventarioanimales__animal = animal).aggregate(
								cantidad = Sum('inventarioanimales__cantidad'),
								cuanto_vende = Sum('inventarioanimales__cuanto_vende'))

		animales.append((animal,conteos['cantidad'],conteos['cuanto_vende']))

	#produccion leche y huevos
	produccion = {}
	for obj in PRODUCCION_CHOICES:
		list_prod = []
		for x in QUIEN_VENDE_CHOICES:
			conteos = filtro.filter(produccionhuevosleche__tipo_produccion = obj[0],produccionhuevosleche__quien_vende = x[0]).aggregate(
									cantidad = Sum('produccionhuevosleche__cantidad'),
									cuanto_vende = Sum('produccionhuevosleche__cuanto_vende'))

			list_prod.append((x[0],conteos['cantidad'],conteos['cuanto_vende']))
		produccion[obj[0]] = list_prod

	#quien vende prod
	quien_vende = {}
	for obj in PRODUCCION_CHOICES2:
		conteo = filtro.filter(vendeproduccion__respuesta__contains = obj[0]).count()
		quien_vende[obj[0]] = conteo,saca_porcentajes(conteo,encuestados,False)

	#agricultura
	#primera
	primera = []
	cultivos_primera = filtro.filter(agricultura__tipo = 'Cultivo de primera').values_list('agricultura__rubro',flat=True)				
	for x in PRODUCCION_CHOICES2:
		for obj in Cultivo.objects.filter(id__in = cultivos_primera):
			cultivo = filtro.filter(agricultura__rubro = obj,agricultura__tipo = 'Cultivo de primera',agricultura__quien_vende = x[0]).aggregate(
						area_sembrada = Sum('agricultura__area_sembrada'),
						produccion_total = Sum('agricultura__produccion_total'),
						semillas = Sum('agricultura__semillas'),
						consumo_humano = Sum('agricultura__consumo_humano'),
						consumo_animal = Sum('agricultura__consumo_animal'),
						venta = Sum('agricultura__venta'),
						costo_produccion = Avg('agricultura__costo_produccion'),
						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
						ganancia_perdida = Avg('agricultura__ganancia_perdida'))

			if cultivo['area_sembrada'] != None:
				primera.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
								cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
								cultivo['venta'],x[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
								cultivo['ganancia_perdida']))

	primera.sort()

	#postrera
	postrera = []
	cultivos_postrera = filtro.filter(agricultura__tipo = 'Cultivo de postrera').values_list('agricultura__rubro',flat=True)
	for x in PRODUCCION_CHOICES2:
		for obj in Cultivo.objects.filter(id__in = cultivos_postrera):
			cultivo = filtro.filter(agricultura__rubro = obj,agricultura__tipo = 'Cultivo de postrera',agricultura__quien_vende = x[0]).aggregate(
						area_sembrada = Sum('agricultura__area_sembrada'),
						produccion_total = Sum('agricultura__produccion_total'),
						semillas = Sum('agricultura__semillas'),
						consumo_humano = Sum('agricultura__consumo_humano'),
						consumo_animal = Sum('agricultura__consumo_animal'),
						venta = Sum('agricultura__venta'),
						costo_produccion = Avg('agricultura__costo_produccion'),
						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
						ganancia_perdida = Avg('agricultura__ganancia_perdida'))
			if cultivo['area_sembrada'] != None:
				postrera.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
							cultivo['venta'],x[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
							cultivo['ganancia_perdida']))
	postrera.sort()

	#apante
	apante = []
	cultivos_apante = filtro.filter(agricultura__tipo = 'Cultivo de apante').values_list('agricultura__rubro',flat=True)
	for x in PRODUCCION_CHOICES2:
		for obj in Cultivo.objects.filter(id__in = cultivos_apante):
			cultivo = filtro.filter(agricultura__rubro = obj,agricultura__tipo = 'Cultivo de apante',agricultura__quien_vende = x[0]).aggregate(
						area_sembrada = Sum('agricultura__area_sembrada'),
						produccion_total = Sum('agricultura__produccion_total'),
						semillas = Sum('agricultura__semillas'),
						consumo_humano = Sum('agricultura__consumo_humano'),
						consumo_animal = Sum('agricultura__consumo_animal'),
						venta = Sum('agricultura__venta'),
						costo_produccion = Avg('agricultura__costo_produccion'),
						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
						ganancia_perdida = Avg('agricultura__ganancia_perdida'))
			if cultivo['area_sembrada'] != None:
				apante.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
							cultivo['venta'],x[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
							cultivo['ganancia_perdida']))
	apante.sort()

	#permanentes
	permanentes = []
	cultivos_permanentes = filtro.filter(agricultura__tipo = 'Cultivos permanentes (Frutales, Cítricos, …)').values_list('agricultura__rubro',flat=True)
	for x in PRODUCCION_CHOICES2:
		for obj in Cultivo.objects.filter(id__in = cultivos_permanentes):
			cultivo = filtro.filter(agricultura__rubro = obj,agricultura__tipo = 'Cultivos permanentes (Frutales, Cítricos, …)',agricultura__quien_vende = x[0]).aggregate(
						area_sembrada = Sum('agricultura__area_sembrada'),
						produccion_total = Sum('agricultura__produccion_total'),
						semillas = Sum('agricultura__semillas'),
						consumo_humano = Sum('agricultura__consumo_humano'),
						consumo_animal = Sum('agricultura__consumo_animal'),
						venta = Sum('agricultura__venta'),
						costo_produccion = Avg('agricultura__costo_produccion'),
						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
						ganancia_perdida = Avg('agricultura__ganancia_perdida'))
			if cultivo['area_sembrada'] != None:
				permanentes.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
							cultivo['venta'],x[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
							cultivo['ganancia_perdida']))
	permanentes.sort()

	#otros
	otros = []
	cultivos_otros = filtro.filter(agricultura__tipo = 'Otros').values_list('agricultura__rubro',flat=True)
	for x in PRODUCCION_CHOICES2:
		for obj in Cultivo.objects.filter(id__in = cultivos_otros):
			cultivo = filtro.filter(agricultura__rubro = obj,agricultura__tipo = 'Otros',agricultura__quien_vende = x[0]).aggregate(
						area_sembrada = Sum('agricultura__area_sembrada'),
						produccion_total = Sum('agricultura__produccion_total'),
						semillas = Sum('agricultura__semillas'),
						consumo_humano = Sum('agricultura__consumo_humano'),
						consumo_animal = Sum('agricultura__consumo_animal'),
						venta = Sum('agricultura__venta'),
						costo_produccion = Avg('agricultura__costo_produccion'),
						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
						ganancia_perdida = Avg('agricultura__ganancia_perdida'))
			if cultivo['area_sembrada'] != None:
				otros.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
							cultivo['venta'],x[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
							cultivo['ganancia_perdida']))
	otros.sort()

	return render(request, template, locals())

@login_required
def organizacion(request,template='frontend/organizacion.html'):
	filtro = _queryset_filtrado(request)
	encuestados = filtro.count()
	conteo_encuesta = filtro.count()

	#cotiza
	cotiza = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(cotizacion__respuesta = obj[0]).count()
		cotiza[obj[0]] = conteo

	#donde cotiza
	donde_cotiza = {}
	for obj in DondeCotiza.objects.all():
		conteo = filtro.filter(respuestasicotiza__donde_cotiza = obj).count()
		donde_cotiza[obj] = conteo

	#desde cuando
	desde_cuando = {}
	for obj in DESDE_CUANDO_CHOICES:
		conteo = filtro.filter(respuestasicotiza__desde_cuando = obj[0]).count()
		desde_cuando[obj[0]] = conteo

	#cuanto cotiza
	mensual = filtro.filter(cotizacion__respuesta = 'Si',respuestasicotiza__frecuencia = 'Mensual').values_list('respuestasicotiza__cuanto_cotiza',flat=True)
	trimestral = filtro.filter(cotizacion__respuesta = 'Si',respuestasicotiza__frecuencia = 'Trimestral').values_list(F('respuestasicotiza__cuanto_cotiza') / 3,flat=True)
	semestral = filtro.filter(cotizacion__respuesta = 'Si',respuestasicotiza__frecuencia = 'Semestral').values_list(F('respuestasicotiza__cuanto_cotiza') / 6,flat=True)
	anual = filtro.filter(cotizacion__respuesta = 'Si',respuestasicotiza__frecuencia = 'Anual').values_list(F('respuestasicotiza__cuanto_cotiza') / 12,flat=True)

	cotizacion_mensual = list(mensual) + list(trimestral) + list(semestral) + list(anual)
	total = sum(cotizacion_mensual)
	promedio = float(total) / len(cotizacion_mensual)

	de_0_50 = 0
	de_51_100 = 0
	de_101_500 = 0
	mas_500 = 0
	cotizaciones = collections.OrderedDict()
	for x in cotizacion_mensual:
		if x <= 50:
			de_0_50 = de_0_50 + 1
		elif x > 50 and x <= 100: 
			de_51_100 = de_51_100 + 1
		elif x > 100 and x <= 500:
			de_101_500 = de_101_500 + 1
		elif x > 500:
			mas_500 = mas_500 + 1

	cotizaciones['0-50'] = de_0_50
	cotizaciones['51-100'] = de_51_100
	cotizaciones['101-500'] = de_101_500
	cotizaciones['> 500'] = mas_500
	
	#frecuencia cotiza
	frecuencia_cotiza = {}
	for obj in FRECUENCIA_CHOICES:
		conteo = filtro.filter(respuestasicotiza__frecuencia = obj[0]).count()
		frecuencia_cotiza[obj[0]] = conteo

	#miembro cooperativa
	cooperativa = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(miembrocooperativa__respuesta = obj[0]).count()
		cooperativa[obj[0]] = conteo

	#cooperativas
	list_cooperativas = {}
	conteo_encu_coop = filtro.filter(miembrocooperativa__respuesta = 'Si',miembrocooperativa__cooperativa__isnull = False).count()
	for obj in Cooperativa.objects.all():
		conteo = filtro.filter(miembrocooperativa__cooperativa = obj).count()
		list_cooperativas[obj] = conteo,saca_porcentajes(conteo,conteo_encu_coop,False)

	#beneficiados proyectos
	beneficiados = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(beneficiadoproyecto__respuesta = obj[0]).count()
		beneficiados[obj[0]] = conteo

	proyectos = {}
	conteo_proy = filtro.filter(beneficiadoproyecto__respuesta = 'Si', beneficiadoproyecto__proyectos__isnull = False).count()
	for obj in Proyecto.objects.all():
		conteo = filtro.filter(beneficiadoproyecto__respuesta = 'Si', beneficiadoproyecto__proyectos = obj).count()
		proyectos[obj] = conteo,saca_porcentajes(conteo,conteo_proy,False)

	#credito
	credito = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(credito__respuesta = obj[0]).count()
		credito[obj[0]] = conteo

	#quien brinda credito
	brinda_credito = []
	for obj in RecibeCredito.objects.all():
		conteo = filtro.filter(credito__respuesta = 'Si', credito__proyectos = obj).count()
		brinda_credito.append((obj,conteo,saca_porcentajes(conteo,encuestados,False)))

	#credito recibido
	tipo_credito = {}
	for obj in FormasCredito.objects.all():
		conteo = filtro.filter(credito__respuesta = 'Si',credito__formas_recibe_credito = obj).count()
		tipo_credito[obj] = conteo

	#problemas productor
	problemas = {}
	for obj in ProblemasProductor.objects.all():
		conteo = filtro.filter(cotizacionorganizacion__problemas_productor = obj).count()
		problemas[obj] = conteo,saca_porcentajes(conteo,encuestados,False)

	#acciones
	acciones = {}
	for obj in CambioClimatico.objects.all():
		conteo = filtro.filter(cotizacionorganizacion__acciones_cambio_climatico = obj).count()
		acciones[obj] = conteo,saca_porcentajes(conteo,encuestados,False)

	#motivos
	motivos = {}
	for obj in AfiliacionUnag.objects.all():
		conteo = filtro.filter(cotizacionorganizacion__afiliacion_unag = obj).count()
		motivos[obj] = conteo,saca_porcentajes(conteo,encuestados,False)


	return render(request, template, locals())

#consulta afiliado

def _queryset_filtrado_datos_afiliado(request):
	params = {}

	if request.session['departamento']:
	    params['afiliado__municipio__departamento__in'] = request.session['departamento']

	if request.session['municipio']:
		params['afiliado__municipio__in'] = request.session['municipio']

	if request.session['comunidad']:
		params['afiliado__comunidad__in'] = request.session['comunidad']

	if request.session['sexo']:
		params['afiliado__sexo'] = request.session['sexo']

	if request.session['estado_civil']:
		params['datosgenerales__estado_civil'] = request.session['estado_civil']

	if request.session['escolaridad']:
		params['escolaridad__escolaridad'] = request.session['escolaridad']

	if request.session['internet']:
		params['datosgenerales__acceso_internet'] = request.session['internet']

	if request.session['cotiza']:
		params['cotizacion__respuesta'] = request.session['cotiza']

	if request.session['cooperativa']:
		params['miembrocooperativa__respuesta'] = request.session['cooperativa']

	if request.session['cooperativas']:
		params['miembrocooperativa__cooperativa__in'] = request.session['cooperativas']

	if request.session['proyecto']:
		params['beneficiadoproyecto__respuesta'] = request.session['proyecto']

	if request.session['credito']:
		params['credito__respuesta'] = request.session['credito']

	if request.session['problemas_productor']:
		params['cotizacionorganizacion__problemas_productor__in'] = request.session['problemas_productor']

	if request.session['cambio_climatico']:
		params['cotizacionorganizacion__acciones_cambio_climatico__in'] = request.session['cambio_climatico']

	if request.session['motivos']:
		params['cotizacionorganizacion__afiliacion_unag__in'] = request.session['motivos']

	unvalid_keys = []
	for key in params:
		if not params[key]:
			unvalid_keys.append(key)

	for key in unvalid_keys:
		del params[key]

	return Encuesta.objects.filter(**params)

@login_required
def consulta_afiliado(request,template='frontend/consulta_datos_afiliados.html'):
	if request.method == 'POST':
		mensaje = None
		form = AfiliadoForm2(request.POST)
		if form.is_valid():
			request.session['departamento'] = form.cleaned_data['departamento']
			request.session['municipio'] = form.cleaned_data['municipio']
			request.session['comunidad'] = form.cleaned_data['comunidad']
			request.session['sexo'] = form.cleaned_data['sexo']
			request.session['estado_civil'] = form.cleaned_data['estado_civil']
			request.session['escolaridad'] = form.cleaned_data['escolaridad']
			request.session['internet'] = form.cleaned_data['internet']
			request.session['cotiza'] = form.cleaned_data['cotiza']
			request.session['cooperativa'] = form.cleaned_data['cooperativa']
			request.session['cooperativas'] = form.cleaned_data['cooperativas']
			request.session['proyecto'] = form.cleaned_data['proyecto']
			request.session['credito'] = form.cleaned_data['credito']
			request.session['problemas_productor'] = form.cleaned_data['problemas_productor']
			request.session['cambio_climatico'] = form.cleaned_data['cambio_climatico']
			request.session['motivos'] = form.cleaned_data['motivos']

			mensaje = "Todas las variables estan correctamente :)"
			request.session['activo'] = True
			centinela = 1
			filtro = _queryset_filtrado_datos_afiliado(request)
			conteo = filtro.count()
		else:
			centinela = 0

	else:
		form = AfiliadoForm2()
		mensaje = "Existen alguno errores"
		try:
			del request.session['departamento']
			del request.session['municipio']
			del request.session['communidad']
			del request.session['sexo']
			del request.session['estado_civil']
			del request.session['escolaridad']
			del request.session['internet']
			del request.session['cotiza']
			del request.session['cooperativa']
			del request.session['cooperativas']
			del request.session['proyecto']
			del request.session['credito']
			del request.session['problemas_productor']
			del request.session['cambio_climatico']
			del request.session['motivos']
		except:
			pass

	return render(request, template, locals())

def tabla_afiliados(request,template='frontend/tabla_afiliados.html'):
	filtro = _queryset_filtrado_datos_afiliado(request)
	conteo = filtro.count()
	lista = []
	for obj in filtro:
		estado_civil = DatosGenerales.objects.filter(encuesta__id = obj.id).values_list('estado_civil',flat=True).last()
		escolaridad = Escolaridad.objects.filter(encuesta__id = obj.id).values_list('escolaridad',flat=True).last()
		if escolaridad == 'Si':
			escolaridad = Escolaridad.objects.filter(encuesta__id = obj.id).values_list('nivel_escolaridad',flat=True).last()

		acceso_internet = Encuesta.objects.filter(id = obj.id).values_list('datosgenerales__acceso_internet', flat=True).last()

		lista.append((obj.afiliado.nombre,obj.afiliado.fecha_nacimiento,str(obj.afiliado.edad) + ' años',
						obj.afiliado.cedula,obj.afiliado.get_sexo_display(),estado_civil,
						obj.afiliado.anio_ingreso,escolaridad,obj.afiliado.lugar_nacimiento,
						obj.afiliado.municipio.departamento.nombre,obj.afiliado.municipio.nombre,
						obj.afiliado.comunidad.nombre,
						str(obj.afiliado.numero_celular) + ' ' + str(obj.afiliado.get_tipo_celular_display()),
						acceso_internet))

	return render(request, template, locals())

def tabla_agrarios(request,template='frontend/tabla_agrarios.html'):
	filtro = _queryset_filtrado_datos_afiliado(request)
	conteo = filtro.count()
	lista = []
	for obj in filtro:
		cotiza = Cotizacion.objects.filter(encuesta__id = obj.id).values_list('respuesta',flat=True).last()
		donde_cotiza = RespuestaSiCotiza.objects.filter(encuesta__id = obj.id).values_list('donde_cotiza__nombre',flat=True).last()
		desde_cuando = RespuestaSiCotiza.objects.filter(encuesta__id = obj.id).values_list('desde_cuando',flat=True).last()
		cuanto_cotiza = RespuestaSiCotiza.objects.filter(encuesta__id = obj.id).values_list('cuanto_cotiza',flat=True).last()
		frecuencia = RespuestaSiCotiza.objects.filter(encuesta__id = obj.id).values_list('frecuencia',flat=True).last()

		miembro = MiembroCooperativa.objects.filter(encuesta__id = obj.id).values_list('respuesta',flat=True).last()
		cooperativa = MiembroCooperativa.objects.filter(encuesta__id = obj.id).values_list('cooperativa__nombre',flat=True)

		beneficiado = BeneficiadoProyecto.objects.filter(encuesta__id = obj.id).values_list('respuesta',flat=True).last()
		proyectos = BeneficiadoProyecto.objects.filter(encuesta__id = obj.id).values_list('proyectos__nombre',flat=True)

		credito = Credito.objects.filter(encuesta__id = obj.id).values_list('respuesta',flat=True).last()
		recibe_credito = Credito.objects.filter(encuesta__id = obj.id).values_list('proyectos__nombre',flat=True).last()
		formas_credito = Credito.objects.filter(encuesta__id = obj.id).values_list('formas_recibe_credito__nombre',flat=True)

		problemas = CotizacionOrganizacion.objects.filter(encuesta__id = obj.id).values_list('problemas_productor__nombre',flat=True)
		acciones = CotizacionOrganizacion.objects.filter(encuesta__id = obj.id).values_list('acciones_cambio_climatico__nombre',flat=True)
		motivos = CotizacionOrganizacion.objects.filter(encuesta__id = obj.id).values_list('afiliacion_unag__nombre',flat=True)

		lista.append((obj.afiliado,	
						cotiza,donde_cotiza,desde_cuando,cuanto_cotiza,frecuencia,
						miembro,cooperativa,beneficiado,proyectos,
						credito,recibe_credito,formas_credito,
						problemas,acciones,motivos))

	return render(request, template, locals())
#ajax
def get_munis(request):
    ids = request.GET.get('ids', '')
    dicc = {}
    resultado = []
    if ids:
        lista = ids.split(',')
        for id in lista:
            try:
                depto = Departamento.objects.get(id = id)
                municipios = Municipio.objects.filter(departamento__id = depto.id).order_by('nombre')
                lista1 = []
                for municipio in municipios:
                    muni = {}
                    muni['id'] = municipio.id
                    muni['nombre'] = municipio.nombre
                    lista1.append(muni)
                    dicc[depto.nombre] = lista1
            except:
                pass

    resultado.append(dicc)

    return HttpResponse(simplejson.dumps(resultado), content_type = 'application/json')

def get_comunies(request):
	ids = request.GET.get('ids', '')
	dicc = {}
	resultado = []
	if ids:
		lista = ids.split(',')
		for id in lista:
			try:
				munici = Municipio.objects.get(id = id)
				encuesta = Afiliado.objects.filter(municipio = munici.id).values_list('comunidad__id',flat=True).distinct()
				comunidades = Comunidad.objects.filter(municipio__id = munici.id,id__in = encuesta).order_by('nombre')
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

def crear_rangos(request, lista, start=0, stop=0, step=0):
	dict_algo = collections.OrderedDict()
	rangos = []
	contador = 0
	rangos = [(n, n+int(step)-1) for n in range(int(start), int(stop), int(step))]

	for desde, hasta in rangos:
		dict_algo['%s a %s' % (desde,hasta)] = len([x for x in lista if desde <= x <= hasta])

	return dict_algo

def obtener_lista(request):
	if request.is_ajax():
		lista = []
		for objeto in Afiliado.objects.all():
			dicc = dict(nombre=objeto.municipio.nombre, id=objeto.id,
						lon=float(objeto.municipio.longitud),
						lat=float(objeto.municipio.latitud)
						)
			lista.append(dicc)

		serializado = simplejson.dumps(lista)
		return HttpResponse(serializado, content_type = 'application/json')

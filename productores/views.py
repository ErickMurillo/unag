# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from productores.forms import *
from django.http import HttpResponse, HttpResponseRedirect
import json as simplejson
from django.db.models import Avg, Sum, F, Count
import collections

# Create your views here.
@login_required
def index(request,template='frontend/index.html'):
	#afiliados
	total_afiliados = Afiliado.objects.all().distinct().count()
	mujeres = Afiliado.objects.filter(sexo = 'Femenino').distinct().count()
	hombres = Afiliado.objects.filter(sexo = 'Masculino').distinct().count()

	#anios encuesta
	years = []
	for en in Encuesta.objects.order_by('anio').values_list('anio', flat=True):
		years.append(en)
	anios = list(sorted(set(years)))

	dic_anios = {}
	for anio in anios:
		#areas
		dic_areas = {}
		for obj in Areas.objects.all():
			areas = AreasFinca.objects.filter(areas = obj,encuesta__anio = anio).aggregate(total = Sum('mz'))['total']
			if areas == None:
				areas = 0

			otras_areas = OtrasTierras.objects.filter(areas = obj,encuesta__anio = anio).aggregate(total = Sum('mz'))['total']
			if otras_areas == None:
				otras_areas = 0

			total = areas + otras_areas
			dic_areas[obj] = total

		#a quien vende prod
		encuestados = Encuesta.objects.filter(anio = anio).distinct().count()
		quien_vende = {}
		for obj in PRODUCCION_CHOICES2:
			conteo = VendeProduccion.objects.filter(respuesta = obj[0]).count()
			if conteo == None:
				conteo = 0

			quien_vende[obj[0]] = conteo,saca_porcentajes(conteo,encuestados,False)

		dic_anios[anio] = dic_areas,quien_vende

	#miembros por dpsto y municipio
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
		hombres_emigran = DatosFamiliares.objects.filter(encuesta__anio = anio,donde_emigran__isnull = False,
							encuesta__afiliado = afiliado.id,sexo = "Masculino").count()

		mujeres_emigran = DatosFamiliares.objects.filter(encuesta__anio = anio,donde_emigran__isnull = False,
							encuesta__afiliado = afiliado.id,sexo = "Femenino").count()

		years[anio] = (hombres,mujeres,ninas,ninos,familiares,hombres_emigran,mujeres_emigran)

	return render(request, template, locals())

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

		legalizada = FormaTenencia.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('legalizada',flat=True)
		documento = DocumentoPropiedad.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('documento__nombre',flat=True)
		agua = SistemaAgua.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('sistema__nombre',flat=True)
		energia = EnergiaElectrica.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('respuesta',flat=True)
		mano_obra = ManoObra.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('mano_obra',flat=True)

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

		years[anio] = (areas,otras,legalizada,documento,agua,energia,mano_obra,tabla_empleo,infraestructura)

	return render(request, template, locals())


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
		for obj in Cultivo.objects.filter(id__in = cultivos_primera):
			cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).aggregate(
						area_sembrada = Sum('agricultura__area_sembrada'),
						produccion_total = Sum('agricultura__produccion_total'),
						semillas = Sum('agricultura__semillas'),
						consumo_humano = Sum('agricultura__consumo_humano'),
						consumo_animal = Sum('agricultura__consumo_animal'),
						venta = Sum('agricultura__venta'),
						costo_produccion = Avg('agricultura__costo_produccion'),
						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
						ganancia_perdida = Avg('agricultura__ganancia_perdida'))

			quien_vende = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).values_list(
													'agricultura__quien_vende',flat=True) 

			primera.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
							cultivo['venta'],quien_vende[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
							cultivo['ganancia_perdida']))


		#postrera
		postrera = []
		cultivos_postrera = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Cultivo de postrera').values_list('agricultura__rubro',flat=True)
		for obj in Cultivo.objects.filter(id__in = cultivos_postrera):
			cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).aggregate(
						area_sembrada = Sum('agricultura__area_sembrada'),
						produccion_total = Sum('agricultura__produccion_total'),
						semillas = Sum('agricultura__semillas'),
						consumo_humano = Sum('agricultura__consumo_humano'),
						consumo_animal = Sum('agricultura__consumo_animal'),
						venta = Sum('agricultura__venta'),
						costo_produccion = Avg('agricultura__costo_produccion'),
						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
						ganancia_perdida = Avg('agricultura__ganancia_perdida'))

			quien_vende = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).values_list(
													'agricultura__quien_vende',flat=True)

			postrera.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
							cultivo['venta'],quien_vende[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
							cultivo['ganancia_perdida']))

		#apante
		apante = []
		cultivos_apante = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Cultivo de apante').values_list('agricultura__rubro',flat=True)
		for obj in Cultivo.objects.filter(id__in = cultivos_apante):
			cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).aggregate(
						area_sembrada = Sum('agricultura__area_sembrada'),
						produccion_total = Sum('agricultura__produccion_total'),
						semillas = Sum('agricultura__semillas'),
						consumo_humano = Sum('agricultura__consumo_humano'),
						consumo_animal = Sum('agricultura__consumo_animal'),
						venta = Sum('agricultura__venta'),
						costo_produccion = Avg('agricultura__costo_produccion'),
						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
						ganancia_perdida = Avg('agricultura__ganancia_perdida'))

			quien_vende = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).values_list(
													'agricultura__quien_vende',flat=True)

			apante.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
							cultivo['venta'],quien_vende[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
							cultivo['ganancia_perdida']))

		#permanentes
		permanentes = []
		cultivos_permanentes = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Cultivos permanentes (Frutales, Cítricos, …)').values_list('agricultura__rubro',flat=True)
		for obj in Cultivo.objects.filter(id__in = cultivos_permanentes):
			cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).aggregate(
						area_sembrada = Sum('agricultura__area_sembrada'),
						produccion_total = Sum('agricultura__produccion_total'),
						semillas = Sum('agricultura__semillas'),
						consumo_humano = Sum('agricultura__consumo_humano'),
						consumo_animal = Sum('agricultura__consumo_animal'),
						venta = Sum('agricultura__venta'),
						costo_produccion = Avg('agricultura__costo_produccion'),
						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
						ganancia_perdida = Avg('agricultura__ganancia_perdida'))

			quien_vende = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).values_list(
													'agricultura__quien_vende',flat=True)

			permanentes.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
							cultivo['venta'],quien_vende[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
							cultivo['ganancia_perdida']))

		#otros
		otros = []
		cultivos_otros = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Otros').values_list('agricultura__rubro',flat=True)
		for obj in Cultivo.objects.filter(id__in = cultivos_otros):
			cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).aggregate(
						area_sembrada = Sum('agricultura__area_sembrada'),
						produccion_total = Sum('agricultura__produccion_total'),
						semillas = Sum('agricultura__semillas'),
						consumo_humano = Sum('agricultura__consumo_humano'),
						consumo_animal = Sum('agricultura__consumo_animal'),
						venta = Sum('agricultura__venta'),
						costo_produccion = Avg('agricultura__costo_produccion'),
						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
						ganancia_perdida = Avg('agricultura__ganancia_perdida'))

			quien_vende = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).values_list(
													'agricultura__quien_vende',flat=True)

			otros.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
							cultivo['venta'],quien_vende[0],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
							cultivo['ganancia_perdida']))
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


	# afiliados = Afiliado.objects.all()

	# if request.GET.get('afiliado'):
	# 	id = request.GET.get('afiliado')
	# 	afiliado = Afiliado.objects.get(id = id)
	# 	escolaridad = Escolaridad.objects.filter(encuesta__afiliado = id).values_list('escolaridad',flat=True).last()

	# 	anios_encuesta = Encuesta.objects.filter(afiliado = afiliado.id).values_list('anio',flat=True)
	# 	estado_civil = Encuesta.objects.filter(afiliado = afiliado.id).values_list('datosgenerales__estado_civil', flat=True).last()
	# 	acceso_internet = Encuesta.objects.filter(afiliado = afiliado.id).values_list('datosgenerales__acceso_internet', flat=True).last()

	# 	# dependen
	# 	last_year = anios_encuesta.last()
	# 	hombres = PersonasDependen.objects.filter(encuesta__afiliado = id,opcion = 'Adultos: Hombres',encuesta__anio = last_year).aggregate(total= Sum('cantidad'))['total']
	# 	mujeres = PersonasDependen.objects.filter(encuesta__afiliado = id,opcion = 'Adultos: Mujeres',encuesta__anio = last_year).aggregate(total= Sum('cantidad'))['total']
	# 	ninas = PersonasDependen.objects.filter(encuesta__afiliado = id,opcion = 'Niñas menores de 12 años',encuesta__anio = last_year).aggregate(total= Sum('cantidad'))['total']
	# 	ninos = PersonasDependen.objects.filter(encuesta__afiliado = id,opcion = 'Niños menores de 12 años',encuesta__anio = last_year).aggregate(total= Sum('cantidad'))['total']

	# 	years = collections.OrderedDict()
	# 	for anio in anios_encuesta:
	# 		#info general
	# 		info = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list(
	# 				'datosgenerales__acceso_internet',
	# 				'datosgenerales__estado_civil',
	# 				'escolaridad__escolaridad',
	# 				'profesion__profecion')

	# 		familiares = []
	# 		for x in DatosFamiliares.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id):
	# 			familiares.append((x.nombres,x.sexo,x.edad,x.escolaridad,x.parentesco))

	# 		emigran = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list(
	# 					'familiaemigra__hombres',
	# 					'familiaemigra__mujeres',
	# 					'familiaemigra__donde_emigran',
	# 					'familiaemigra__tiempo',
	# 					'familiaemigra__meses')

	# 		areas = {}
	# 		otras = {}
	# 		for obj in Areas.objects.all():
	# 			areas_finca = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,areasfinca__areas = obj).values_list(
	# 					'areasfinca__mz',flat=True)
	# 			areas[obj] = areas_finca

	# 			otras_areas = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,otrastierras__areas = obj).values_list(
	# 					'otrastierras__mz',flat=True)
	# 			otras[obj] = otras_areas

	# 		origen_propiedad = OrigenPropiedad.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('opcion__nombre',flat=True)
	# 		legalizada = FormaTenencia.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('legalizada',flat=True)
	# 		documento = DocumentoPropiedad.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('documento__nombre',flat=True)
	# 		agua = SistemaAgua.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('sistema__nombre',flat=True)
	# 		energia = EnergiaElectrica.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('respuesta',flat=True)
	# 		mano_obra = ManoObra.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('mano_obra',flat=True)

	# 		tabla_empleo = []
	# 		empleo = TablaEmpleo.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id)
	# 		rubro = empleo.values_list('rubro__nombre',flat=True).distinct()
	# 		for obj in rubro:
	# 			cont = empleo.filter(rubro__nombre = obj).aggregate(
	# 					temporal_hombres = Sum('temporal_hombres'),
	# 					temporal_mujeres = Sum('temporal_mujeres'),
	# 					permanente_hombres = Sum('permanente_hombres'),
	# 					permanente_mujeres = Sum('permanente_mujeres'),
	# 					familiar_hombres = Sum('familiar_hombres'),
	# 					familiar_mujeres = Sum('familiar_mujeres'))

	# 			tabla_empleo.append((obj,cont['temporal_hombres'],cont['temporal_mujeres'],
	# 										cont['permanente_hombres'],cont['permanente_mujeres'],
	# 										cont['familiar_hombres'],cont['familiar_mujeres']))

	# 		infraestructura = Infraestructura.objects.filter(encuesta__anio = anio,encuesta__afiliado = afiliado.id).values_list('tipo__nombre',flat=True)

	# 		#agricultura
	# 		#primera
	# 		primera = []
	# 		cultivos_primera = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Cultivo de primera').values_list('agricultura__rubro',flat=True)
	# 		for obj in Cultivo.objects.filter(id__in = cultivos_primera):
	# 			cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).aggregate(
	# 						area_sembrada = Sum('agricultura__area_sembrada'),
	# 						produccion_total = Sum('agricultura__produccion_total'),
	# 						semillas = Sum('agricultura__semillas'),
	# 						consumo_humano = Sum('agricultura__consumo_humano'),
	# 						consumo_animal = Sum('agricultura__consumo_animal'),
	# 						venta = Sum('agricultura__venta'),
	# 						costo_produccion = Avg('agricultura__costo_produccion'),
	# 						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
	# 						ganancia_perdida = Avg('agricultura__ganancia_perdida'))

	# 			primera.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
	# 							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
	# 							cultivo['venta'],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
	# 							cultivo['ganancia_perdida']))


	# 		#postrera
	# 		postrera = []
	# 		cultivos_postrera = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Cultivo de postrera').values_list('agricultura__rubro',flat=True)
	# 		for obj in Cultivo.objects.filter(id__in = cultivos_postrera):
	# 			cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).aggregate(
	# 						area_sembrada = Sum('agricultura__area_sembrada'),
	# 						produccion_total = Sum('agricultura__produccion_total'),
	# 						semillas = Sum('agricultura__semillas'),
	# 						consumo_humano = Sum('agricultura__consumo_humano'),
	# 						consumo_animal = Sum('agricultura__consumo_animal'),
	# 						venta = Sum('agricultura__venta'),
	# 						costo_produccion = Avg('agricultura__costo_produccion'),
	# 						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
	# 						ganancia_perdida = Avg('agricultura__ganancia_perdida'))

	# 			postrera.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
	# 							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
	# 							cultivo['venta'],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
	# 							cultivo['ganancia_perdida']))

	# 		#apante
	# 		apante = []
	# 		cultivos_apante = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Cultivo de apante').values_list('agricultura__rubro',flat=True)
	# 		for obj in Cultivo.objects.filter(id__in = cultivos_apante):
	# 			cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).aggregate(
	# 						area_sembrada = Sum('agricultura__area_sembrada'),
	# 						produccion_total = Sum('agricultura__produccion_total'),
	# 						semillas = Sum('agricultura__semillas'),
	# 						consumo_humano = Sum('agricultura__consumo_humano'),
	# 						consumo_animal = Sum('agricultura__consumo_animal'),
	# 						venta = Sum('agricultura__venta'),
	# 						costo_produccion = Avg('agricultura__costo_produccion'),
	# 						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
	# 						ganancia_perdida = Avg('agricultura__ganancia_perdida'))

	# 			apante.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
	# 							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
	# 							cultivo['venta'],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
	# 							cultivo['ganancia_perdida']))

	# 		#permanentes
	# 		permanentes = []
	# 		cultivos_permanentes = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Cultivos permanentes (Frutales, Cítricos, …)').values_list('agricultura__rubro',flat=True)
	# 		for obj in Cultivo.objects.filter(id__in = cultivos_permanentes):
	# 			cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).aggregate(
	# 						area_sembrada = Sum('agricultura__area_sembrada'),
	# 						produccion_total = Sum('agricultura__produccion_total'),
	# 						semillas = Sum('agricultura__semillas'),
	# 						consumo_humano = Sum('agricultura__consumo_humano'),
	# 						consumo_animal = Sum('agricultura__consumo_animal'),
	# 						venta = Sum('agricultura__venta'),
	# 						costo_produccion = Avg('agricultura__costo_produccion'),
	# 						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
	# 						ganancia_perdida = Avg('agricultura__ganancia_perdida'))

	# 			permanentes.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
	# 							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
	# 							cultivo['venta'],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
	# 							cultivo['ganancia_perdida']))

	# 		#otros
	# 		otros = []
	# 		cultivos_otros = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__tipo = 'Otros').values_list('agricultura__rubro',flat=True)
	# 		for obj in Cultivo.objects.filter(id__in = cultivos_otros):
	# 			cultivo = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,agricultura__rubro = obj).aggregate(
	# 						area_sembrada = Sum('agricultura__area_sembrada'),
	# 						produccion_total = Sum('agricultura__produccion_total'),
	# 						semillas = Sum('agricultura__semillas'),
	# 						consumo_humano = Sum('agricultura__consumo_humano'),
	# 						consumo_animal = Sum('agricultura__consumo_animal'),
	# 						venta = Sum('agricultura__venta'),
	# 						costo_produccion = Avg('agricultura__costo_produccion'),
	# 						ingresos_produccion = Avg('agricultura__ingresos_produccion'),
	# 						ganancia_perdida = Avg('agricultura__ganancia_perdida'))

	# 			otros.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
	# 							cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
	# 							cultivo['venta'],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
	# 							cultivo['ganancia_perdida']))
	# 		#inventario animales
	# 		animales = []
	# 		for animal in Animales.objects.all():
	# 			conteos = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,inventarioanimales__animal = animal).aggregate(
	# 									cantidad = Sum('inventarioanimales__cantidad'),
	# 									cuanto_vende = Sum('inventarioanimales__cuanto_vende'))

	# 			animales.append((animal,conteos['cantidad'],conteos['cuanto_vende']))

	# 		#produccion leche y huevos
	# 		produccion = {}
	# 		for obj in PRODUCCION_CHOICES:
	# 			list_prod = []
	# 			for x in QUIEN_VENDE_CHOICES:
	# 				conteos = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id,produccionhuevosleche__tipo_produccion = obj[0],produccionhuevosleche__quien_vende = x[0]).aggregate(
	# 										cantidad = Sum('produccionhuevosleche__cantidad'),
	# 										cuanto_vende = Sum('produccionhuevosleche__cuanto_vende'))

	# 				list_prod.append((x[0],conteos['cantidad'],conteos['cuanto_vende']))
	# 			produccion[obj[0]] = list_prod

	# 		quien_vende = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('vendeproduccion__respuesta',flat=True)

	# 		#organizacion
	# 		cotiza = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('cotizacion__respuesta',flat=True)
	# 		si_cotiza = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list(
	# 						'respuestasicotiza__donde_cotiza__nombre','respuestasicotiza__desde_cuando',
	# 						'respuestasicotiza__cuanto_cotiza','respuestasicotiza__frecuencia')

	# 		cooperativa = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('miembrocooperativa__respuesta',flat=True)
	# 		list_cooperativas = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('miembrocooperativa__cooperativa__nombre',flat=True)

	# 		proyecto = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('beneficiadoproyecto__respuesta',flat=True)
	# 		list_proyectos = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('beneficiadoproyecto__proyectos__nombre',flat=True)

	# 		credito = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('credito__respuesta','credito__proyectos__nombre')
	# 		list_credito = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('credito__formas_recibe_credito__nombre',flat=True)

	# 		problemas = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('cotizacionorganizacion__problemas_productor__nombre',flat=True)

	# 		acciones = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('cotizacionorganizacion__acciones_cambio_climatico__nombre',flat=True)

	# 		motivos_afiliacion = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('cotizacionorganizacion__afiliacion_unag__nombre',flat=True)

	# 		comentarios = Encuesta.objects.filter(anio = anio,afiliado = afiliado.id).values_list('cotizacionorganizacion__comentarios',flat=True)

	# 		years[anio] = (info,familiares,emigran,areas,otras,origen_propiedad,legalizada,documento,agua,energia,
	# 						mano_obra,tabla_empleo,infraestructura,primera,postrera,apante,permanentes,otros,
	# 						animales,produccion,quien_vende,cotiza,si_cotiza,cooperativa,list_cooperativas,
	# 						proyecto,list_proyectos,credito,list_credito,problemas,acciones,motivos_afiliacion,
	# 						comentarios)

	# 	consulta = 1
	# else:
	# 	consulta = 0

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
	periodo = collections.OrderedDict()
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
	list_areas = filtro.values_list('areasfinca__areas',flat=True)
	for obj in Areas.objects.filter(id__in = list_areas):
		areas = filtro.filter(areasfinca__areas = obj.id).aggregate(suma = Sum('areasfinca__mz'))['suma']
		areas_finca[obj] = areas

	#otras areas
	otras_areas_finca = {}
	otras_areas = filtro.values_list('otrastierras__areas',flat=True)
	for obj in Areas.objects.filter(id__in = otras_areas):
		areas = filtro.filter(otrastierras__areas = obj.id).aggregate(suma = Sum('otrastierras__mz'))['suma']
		otras_areas_finca[obj] = areas

	#origen propiedad
	propiedad = {}
	list_origen = filtro.values_list('origenpropiedad__opcion',flat=True)
	for obj in Origen.objects.filter(id__in = list_origen):
		conteo = filtro.filter(origenpropiedad__opcion = obj.id).count()
		propiedad[obj] = conteo

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

	return render(request, template, locals())

def datos_produccion(request,template='frontend/datos_produccion.html'):
	filtro = _queryset_filtrado(request)
	encuestados = filtro.count()

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
	for obj in Cultivo.objects.filter(id__in = cultivos_primera):
		cultivo = filtro.filter(agricultura__rubro = obj).aggregate(
					area_sembrada = Sum('agricultura__area_sembrada'),
					produccion_total = Sum('agricultura__produccion_total'),
					semillas = Sum('agricultura__semillas'),
					consumo_humano = Sum('agricultura__consumo_humano'),
					consumo_animal = Sum('agricultura__consumo_animal'),
					venta = Sum('agricultura__venta'),
					costo_produccion = Avg('agricultura__costo_produccion'),
					ingresos_produccion = Avg('agricultura__ingresos_produccion'),
					ganancia_perdida = Avg('agricultura__ganancia_perdida'))

		primera.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
						cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
						cultivo['venta'],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
						cultivo['ganancia_perdida']))

	#postrera
	postrera = []
	cultivos_postrera = filtro.filter(agricultura__tipo = 'Cultivo de postrera').values_list('agricultura__rubro',flat=True)
	for obj in Cultivo.objects.filter(id__in = cultivos_postrera):
		cultivo = filtro.filter(agricultura__rubro = obj).aggregate(
					area_sembrada = Sum('agricultura__area_sembrada'),
					produccion_total = Sum('agricultura__produccion_total'),
					semillas = Sum('agricultura__semillas'),
					consumo_humano = Sum('agricultura__consumo_humano'),
					consumo_animal = Sum('agricultura__consumo_animal'),
					venta = Sum('agricultura__venta'),
					costo_produccion = Avg('agricultura__costo_produccion'),
					ingresos_produccion = Avg('agricultura__ingresos_produccion'),
					ganancia_perdida = Avg('agricultura__ganancia_perdida'))

		postrera.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
						cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
						cultivo['venta'],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
						cultivo['ganancia_perdida']))

	#apante
	apante = []
	cultivos_apante = filtro.filter(agricultura__tipo = 'Cultivo de apante').values_list('agricultura__rubro',flat=True)
	for obj in Cultivo.objects.filter(id__in = cultivos_apante):
		cultivo = filtro.filter(agricultura__rubro = obj).aggregate(
					area_sembrada = Sum('agricultura__area_sembrada'),
					produccion_total = Sum('agricultura__produccion_total'),
					semillas = Sum('agricultura__semillas'),
					consumo_humano = Sum('agricultura__consumo_humano'),
					consumo_animal = Sum('agricultura__consumo_animal'),
					venta = Sum('agricultura__venta'),
					costo_produccion = Avg('agricultura__costo_produccion'),
					ingresos_produccion = Avg('agricultura__ingresos_produccion'),
					ganancia_perdida = Avg('agricultura__ganancia_perdida'))

		apante.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
						cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
						cultivo['venta'],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
						cultivo['ganancia_perdida']))

	#permanentes
	permanentes = []
	cultivos_permanentes = filtro.filter(agricultura__tipo = 'Cultivos permanentes (Frutales, Cítricos, …)').values_list('agricultura__rubro',flat=True)
	for obj in Cultivo.objects.filter(id__in = cultivos_permanentes):
		cultivo = filtro.filter(agricultura__rubro = obj).aggregate(
					area_sembrada = Sum('agricultura__area_sembrada'),
					produccion_total = Sum('agricultura__produccion_total'),
					semillas = Sum('agricultura__semillas'),
					consumo_humano = Sum('agricultura__consumo_humano'),
					consumo_animal = Sum('agricultura__consumo_animal'),
					venta = Sum('agricultura__venta'),
					costo_produccion = Avg('agricultura__costo_produccion'),
					ingresos_produccion = Avg('agricultura__ingresos_produccion'),
					ganancia_perdida = Avg('agricultura__ganancia_perdida'))

		permanentes.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
						cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
						cultivo['venta'],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
						cultivo['ganancia_perdida']))

	#otros
	otros = []
	cultivos_otros = filtro.filter(agricultura__tipo = 'Otros').values_list('agricultura__rubro',flat=True)
	for obj in Cultivo.objects.filter(id__in = cultivos_otros):
		cultivo = filtro.filter(agricultura__rubro = obj).aggregate(
					area_sembrada = Sum('agricultura__area_sembrada'),
					produccion_total = Sum('agricultura__produccion_total'),
					semillas = Sum('agricultura__semillas'),
					consumo_humano = Sum('agricultura__consumo_humano'),
					consumo_animal = Sum('agricultura__consumo_animal'),
					venta = Sum('agricultura__venta'),
					costo_produccion = Avg('agricultura__costo_produccion'),
					ingresos_produccion = Avg('agricultura__ingresos_produccion'),
					ganancia_perdida = Avg('agricultura__ganancia_perdida'))

		otros.append((obj.nombre,cultivo['area_sembrada'],cultivo['produccion_total'],
						cultivo['semillas'],cultivo['consumo_humano'],cultivo['consumo_animal'],
						cultivo['venta'],cultivo['costo_produccion'],cultivo['ingresos_produccion'],
						cultivo['ganancia_perdida']))

	return render(request, template, locals())

def organizacion(request,template='frontend/organizacion.html'):
	filtro = _queryset_filtrado(request)
	encuestados = filtro.count()

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
	lista = filtro.filter(cotizacion__respuesta = 'Si').values_list('respuestasicotiza__cuanto_cotiza',flat=True)
	try:
		minimo = min(lista)
	except:
		minimo = 0

	try:
		maximo = max(lista)
	except:
		maximo = 0

	cuanto_cotiza = crear_rangos(request, lista, minimo, maximo, step=50)

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
	for obj in Cooperativa.objects.all():
		conteo = filtro.filter(miembrocooperativa__cooperativa = obj).count()
		list_cooperativas[obj] = conteo,saca_porcentajes(conteo,encuestados,False)

	#beneficiados proyectos
	beneficiados = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(beneficiadoproyecto__respuesta = obj[0]).count()
		beneficiados[obj[0]] = conteo

	proyectos = {}
	for obj in Proyecto.objects.all():
		conteo = filtro.filter(beneficiadoproyecto__respuesta = 'Si', beneficiadoproyecto__proyectos = obj).count()
		proyectos[obj] = conteo,saca_porcentajes(conteo,encuestados,False)

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

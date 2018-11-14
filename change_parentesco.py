# -*- coding: utf-8 -*-
from productores.models import *

lista = ['Cuñada','Cuñado','Tía','Tío']
query = DatosFamiliares.objects.filter(parentesco__in = lista)

for x in query:
	if x.parentesco == u'Cuñada':
		x.parentesco = u'Cuniada'
	elif x.parentesco == u'Cuñado':
		x.parentesco = u'Cuniado'
	elif x.parentesco == u'Tía':
		x.parentesco = u'Tia'
	elif x.parentesco == u'Tío':
		x.parentesco = u'Tio'

	x.save()
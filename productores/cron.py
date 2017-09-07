from .models import *

def my_scheduled_job():
  afiliados = Afiliados.objects.all()
  for obj in afiliados:
  	obj.save()
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from lugar.models import *
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.
SEXO_CHOICES = (('Femenino','Femenino'), ('Masculino','Masculino'))
CELULAR_CHOICES = (('Movistar','Movistar'), ('Claro','Claro'))
SI_NO_CHOICES = (('Si','Si'), ('No','No'))
ESTADO_CIVIL_CHOICES = (('Soltero(a)','Soltero(a)'), ('Casado(a)','Casado(a)'), ('Acompañado(a)','Acompañado(a)'),
                        ('Viudo(a)','Viudo(a)'), ('Divorciado(a)','Divorciado(a)'))

class Afiliado(models.Model):
    municipio = models.ForeignKey(Municipio)
    comunidad = ChainedForeignKey(
                                Comunidad,
                                chained_field="municipio",
                                chained_model_field="municipio",
                                show_all=False, auto_choose=True)
    nombre = models.CharField(max_length=200)
    cedula = models.CharField(max_length=20,verbose_name='Cédula',null=True,blank=True,unique=True)
    sexo = models.CharField(max_length=20,choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField()
    lugar_nacimiento = models.ForeignKey(Departamento)
    anio_ingreso = models.IntegerField()
    numero_celular = models.CharField(max_length=20)
    tipo_celular = models.CharField(max_length=20,choices=CELULAR_CHOICES)
    acceso_internet = models.CharField(max_length=20,choices=SI_NO_CHOICES)
    estado_civil = models.CharField(max_length=20,choices=ESTADO_CIVIL_CHOICES)

    class Meta:
        verbose_name_plural = 'I. Datos generales del/la afiliado/a'

ESCOLARIDAD_CHOICES = (('Alfabetizado','Alfabetizado'), ('Lee y Escribe','Lee y Escribe'), ('Primaria','Primaria'),
                        ('Secundaria','Secundaria'), ('Universitario','Universitario'))

class Escolaridad(models.Model):
    afiliado = models.ForeignKey(Afiliado)
    escolaridad = models.CharField(max_length=20,choices=ESCOLARIDAD_CHOICES)
    respuesta = models.CharField(max_length=20,choices=SI_NO_CHOICES)

    class Meta:
        verbose_name = 'Escolaridad'

class Profesion(models.Model):
    afiliado = models.ForeignKey(Afiliado)
    profecion = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Profesión'

PERSONAS_CHOICES = (('Total','Total'),('Adultos: Hombres','Adultos: Hombres'),('Adultos: Mujeres','Adultos: Mujeres'),
                    ('Niñas menores de 12 años','Niñas menores de 12 años'),('Niños menores de 12 años','Niños menores de 12 años'))

class PersonasDependen(models.Model):
    afiliado = models.ForeignKey(Afiliado)
    opcion = models.CharField(max_length=25,choices=PERSONAS_CHOICES)
    cantidad = models.IntegerField()

    class Meta:
        verbose_name = 'Personas que dependen del afiliado'
